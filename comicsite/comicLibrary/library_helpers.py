import threading
import shutil
import os
import re
import subprocess
from comicsite.settings import MEDIA_ROOT, COMIC_TEMP_FOLDER
from exceptions import Exception
#global lock for the comic_cache index
library_cache_lock = None
# Cache list
CACHE_SIZE = 10
comic_cache = None

#File types
CBR = 1
CBZ = 2

extractors = {
        CBR: " ".join((subprocess.check_output(['which', 'unrar']).strip(), 'e')),
        CBZ: subprocess.check_output(['which', 'unzip']).strip(),
        }

def NoExtractoException(Exception):pass

def get_extractor(archive):
    arc_name = archive.strip()
    if arc_name.endswith('cbr') or arc_name.endswith('CBR'):
        return extractors[CBR]
    elif arc_name.endswith('cbz') or arc_name.endswith('CBZ'):
        return extractors[CBZ]
    else:
        raise NoExtractoException("No extractor found for %s" % archive)


class ComicCacheEntry(object):
    def __init__(self,comic):
        self.pages_list = list()
        self.comic_name = comic.archive.name
        self.dir_name = self.create_temp_dir(self.comic_name)
        self.extract_comic(comic.archive.file.name)
        # at this point we have all the pages in the pages_list sorted

    def create_temp_dir(self, comic_name):
        dir_name = COMIC_TEMP_FOLDER+comic_name
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return dir_name

    def extract_comic(self, archive):
        # Old Version
        #New Version
        extractor = get_extractor(archive)
        current_dir = os.getcwd()
        os.chdir(self.dir_name)
        command_line = "%s \"%s\"" %(extractor, archive)
        subprocess.Popen(command_line,shell=True).wait()
        self.pages_list = [p for p in os.listdir('.') if p.lower().endswith("jpg")]
        os.chdir(current_dir)
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
        print("Removing {0}".format(old_entry.dir_name))
        shutil.rmtree(old_entry.dir_name)
    return new_entry.get_page(page_num)

#initialization of the global settings
if not library_cache_lock:
    library_cache_lock = threading.Lock()
    shutil.rmtree(COMIC_TEMP_FOLDER, ignore_errors=True) # if it is not there, no worries
    comic_cache = list()
