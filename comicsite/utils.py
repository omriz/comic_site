#!/usr/bin/env python
import os
import sys
import inspect
import logging
import re

#Specific Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comicsite.settings")
from comicLibrary.models import Comic, ComicSeries

ISSUE_RE = re.compile("^\D+(\d+)")

def create_comic(path, issue, series):
    new_comic = Comic(series=series, issue=issue, archive=path)
    new_comic.save()
    return new_comic

def get_series(series):
    return ComicSeries.objects.get_or_create(series=series)[0]

def get_series_name(dir_path):
    if os.path.exists(os.path.join(dir_path, ".SERIES")):
        with open(os.path.join(dir_path, ".SERIES")) as series_file:
            series = series_file.readline().strip()
    else:
        series = " ".join(os.path.split(dir_path)[-1].split("_"))
    return series

def update_single_file(file_path):
    root_dir = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    file_abs_path = os.path.abspath(file_path)
    rel_file_path = file_abs_path.rsplit(root_dir+"/media/")[-1]
    print file_path, rel_file_path
    if not os.path.exists(file_path) or not rel_file_path:
        print("File does not exist or path problem")
        sys.exit(-1)
    dir_path, comic_file = os.path.split(file_path)
    series_name = get_series(get_series_name(dir_path))
    res = ISSUE_RE.match(comic_file)
    if res:
        issue = int(res.groups()[0])
        create_comic(rel_file_path, issue, series_name)
    else:
        logging.error("Could not figure out commic issue")
        sys.exit(1)

