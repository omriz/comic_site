#!/usr/bin/env python
import os
import sys
from comicLibrary.models import Comic, ComicSeries

def create_series(name):
    new_series = ComicSeries(series=name)
    new_series.save()
    return new_series

def create_comic(path, issue, series):
    new_comic = Comic(series=series, issue=issue, archive=path)
    new_comic.save()
    return new_comic

def update_files():
    pass
    
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comicsite.settings")
    from django.core.management import execute_from_command_line
    update_files()