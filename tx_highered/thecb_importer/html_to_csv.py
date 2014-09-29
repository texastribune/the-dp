#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage: html_to_csv.py FILE

Convert an excel html file to csv on stdout. Similar to "in2csv", except in2csv
does not support this format.

Arguments:
  FILE  one *.xls.html file from THECB
"""

import os
import sys

from csvkit import CSVKitDictWriter
from docopt import docopt
from lxml import html as etree


def parse_html(path):
    html = etree.parse(path)
    row_iter = iter(html.xpath('//tr'))

    # Throw away the report header in the first row
    first_row = next(row_iter)
    if len(first_row.getchildren()) == 1:
        first_row = next(row_iter)

    # The column names are in the second row
    header = [col.text_content() for col in first_row]

    # Parse dict records from the remaining rows
    data = []
    for row in row_iter:
        values = [c.text.strip().strip('%') if c.text else None for c in row]
        values = [v if v != 'N/A' else None for v in values]
        record = dict(zip(header, values))
        data.append(record)

    return header, data


def html_to_csv(path):
    header, data = parse_html(path)

    # Create stdout writer
    header.insert(2, 'System')
    writer = CSVKitDictWriter(sys.stdout, header)
    writer.writeheader()

    # Parse ID and system before writing each row
    for row in data:
        id_field = row.pop('FICE')
        if not id_field:
            continue

        # Parse out System that may be in parenthesis in the FICE field
        fice_parts = id_field.split(' (')
        row['FICE'] = fice_parts[0]
        if len(fice_parts) > 1:
            row['System'] = fice_parts[1].strip(') ')
        else:
            row['System'] = None

        writer.writerow(row)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if not os.path.exists(arguments['FILE']):
        exit("File does not exist")
    html_to_csv(arguments['FILE'])
