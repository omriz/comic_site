#!/usr/bin/env python
import os
import sys
import inspect
import logging
import re

#Specific Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comicsite.settings")
from comicLibrary.models import Comic, ComicSeries

ISSUE_RE = re.compile("^(\D+)\s*(\d+)")
SPACES = (" ", "_", "\t", "\n", "#")

def create_comic(path, series, issue, annual=False):
    new_comic = Comic(series=series, issue=issue, archive=path, annual = annual)
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
    if not os.path.exists(file_path) or not rel_file_path:
        print("File does not exist or path problem")
        sys.exit(-1)
    dir_path, comic_file = os.path.split(file_path)
    comic_name, issue, annual = extract_comic_info(comic_file)
    if comic_name is None and issue is None and annual is None:
        return
    create_comic(rel_file_path, get_series(comic_name), issue, annual)

def extract_comic_info(file_name):
    file_name = file_name.split(".")[0].lower()
    loc = file_name.find("annual")
    if loc != -1:
        annual = True
        file_name = file_name[:loc]+file_name[loc+len("annual"):]
    else:
        annual = False
    name = ""
    capitlize = True
    for c in file_name:
        if c in SPACES:
            if not capitlize:
                capitlize = True
                name += " "
        else:
            if capitlize:
                name += c.upper()
                capitlize = False
            else:
                name += c
    x = ISSUE_RE.match(name)
    if x:
        comic_name = x.groups()[0].strip()
        issue = int(x.groups()[1])
        return comic_name, issue, annual
    else:
        return None, None, None
