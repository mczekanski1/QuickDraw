"""
Takes all csv files in a directory and combines them into one large csv file.
"""

import os
import sys
import shutil

if sys.argv[1][-1] != "/":
    DATA_DIR = sys.argv[1] + "/"
else:
    DATA_DIR = sys.argv[1]

csv_files = [file for file in os.listdir(DATA_DIR) if file.find(".csv") != -1]

print(csv_files)

with open(sys.argv[2], "w") as out:
    for file in csv_files:
        with open(DATA_DIR + file) as f:
            next(f)   # skip header
            shutil.copyfileobj(f, out)
