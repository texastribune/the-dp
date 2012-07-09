#! /usr/bin/env python

# Usage: ./load.py /path/to/DC_MasterFile_79930.mvl

import sys

from ipeds_importer.models import Variable

path = sys.argv[1]

print path
print Variable.objects.count()

with open(path, "r") as f:
    for row in f:
        bits = row.split('|')
        code, short_name, category, long_name = bits[0:4]
        data = dict(code=code,
                    short_name=short_name,
                    category=category,
                    long_name=long_name)
        Variable.objects.get_or_create(raw=row, defaults=data)
print Variable.objects.count()
