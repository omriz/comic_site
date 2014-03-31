#!/usr/bin/env python
import os
import argparse
import re

#Specific Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comicsite.settings")
from comicLibrary.models import Comic, ComicSeries


def create_comic(path, issue, series):
    new_comic = Comic(series=series, issue=issue, archive=path)
    new_comic.save()
    return new_comic


def update_files():
    parser = argparse.ArgumentParser(description="Library updater argument parser")
    parser.add_argument('--dir', nargs="?")
    parser.add_argument('--series', nargs="?")
    args = parser.parse_args()
    comic_dir = "/".join(args.dir.split("/")[1:])
    series = ComicSeries.objects.get_or_create(series=args.series)[0]
    comp_re = re.compile("^\D+(\d+)")
    for comic in os.listdir(args.dir):
        res = comp_re.match(comic)
        if res:
            issue = int(res.groups()[0])
            new_comic = create_comic(os.path.join(comic_dir, comic), issue, series)
            print("Added {0}".format(new_comic))
    series.save()

    pass
    
if __name__ == "__main__":
    #from django.core.management import execute_from_command_line
    update_files()