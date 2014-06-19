#!/usr/bin/env python
import os
import argparse
import re
from utils import ISSUE_RE, create_comic, get_series, extract_comic_info

def update_files():
    parser = argparse.ArgumentParser(description="Library updater argument parser")
    parser.add_argument('--dir', nargs="?")
    args = parser.parse_args()
    comic_dir = "/".join(args.dir.split("/")[1:])
    for comic in os.listdir(args.dir):
        comic_name, issue, annual = extract_comic_info(comic)
        if comic_name is None and issue is None and annual is None:
            continue
        series = get_series(comic_name)
        new_comic = create_comic(os.path.join(comic_dir, comic), series, issue, annual)
        print("Added {0}".format(new_comic))
    series.save()
    
if __name__ == "__main__":
    #from django.core.management import execute_from_command_line
    update_files()
