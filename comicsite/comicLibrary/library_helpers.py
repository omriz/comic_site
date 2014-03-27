import threading
import shutil
import os
import re
from comicsite.settings import MEDIA_ROOT, COMIC_TEMP_FOLDER
from comicLibrary.archive import Extractor
#global lock for the comic_cache index
library_cache_lock = None
# Cache list
CACHE_SIZE = 10
comic_cache = None

class ComicCacheEntry(object):
    def __init__(self,comic):
        self.pages_list = list()
        self.comic_name = comic.archive.name
        self.dir_name = self.create_temp_dir(self.comic_name)
        self.extract_comic(comic.archive.file.name)
        # at this point we have all the pages in the pages_list sorted

    def create_temp_dir(self, comic_name):
        dir_name = COMIC_TEMP_FOLDER+comic_name
        os.makedirs(dir_name, exist_ok=True)
        return dir_name

    def extract_comic(self, archive):
        extractor = Extractor()
        extractor.setup(archive, self.dir_name)
        extractor.extract()
        extractor.wait()
        self.pages_list = [p for p in extractor.get_files() if p.endswith("jpg")]
        alphanumeric_sort(self.pages_list)

    def get_page(self, page_num):
        if page_num > len(self.pages_list) :
            return None
        else:
            #This is proportional to the static directory
            return os.path.join(self.comic_name,self.pages_list[page_num-1])

def alphanumeric_sort(filenames):
    """Do an in-place alphanumeric sort of the strings in <filenames>,
    such that for an example "1.jpg", "2.jpg", "10.jpg" is a sorted
    ordering.
    """
    rec = re.compile("\d+|\D+")
    def _format_substrings(name):
        strings = rec.findall(name)
        my_list = list()
        for s in strings:
            if s.isdigit():
                my_list.append(int(s))
            my_list.append(s.lower())
        return my_list
    filenames.sort(key=_format_substrings)

def get_comic_page(comic, page_num):
    for entry in comic_cache:
        if entry.comic_name == comic.archive.name:
            return entry.get_page(page_num)
    new_entry = ComicCacheEntry(comic)
    library_cache_lock.acquire(True) #blocking
    if len(comic_cache) >= CACHE_SIZE:
        old_entry = comic_cache.pop(0)
    else:
        old_entry = None
    comic_cache.append(new_entry)
    library_cache_lock.release()
    if old_entry:
        shutil.rmtree(old_entry.dir_name)
    return new_entry.get_page(page_num)

#initialization of the global settings
if not library_cache_lock:
    library_cache_lock = threading.Lock()
    comic_cache = list()
