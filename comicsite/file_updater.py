#!/usr/bin/env python
import os
import argparse
import re
from utils import ISSUE_RE, create_comic, get_series

def update_files():
    parser = argparse.ArgumentParser(description="Library updater argument parser")
    parser.add_argument('--dir', nargs="?")
    parser.add_argument('--series', nargs="?")
    args = parser.parse_args()
    comic_dir = "/".join(args.dir.split("/")[1:])
    series = get_series(args.series)
    for comic in os.listdir(args.dir):
        res = ISSUE_RE.match(comic)
        if res:
            issue = int(res.groups()[0])
            new_comic = create_comic(os.path.join(comic_dir, comic), issue, series)
            print("Added {0}".format(new_comic))
    series.save()

    pass
    
if __name__ == "__main__":
    #from django.core.management import execute_from_command_line
    update_files()
