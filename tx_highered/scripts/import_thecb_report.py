#! /usr/bin/env python
"""
Import from the Accountability report system

TODO what is this for? How come this only does top 10 percent?
"""
from collections import namedtuple
from csv import reader
import os
import re
import sys

from lxml import html as etree

from tx_highered.models import Institution


# Similar to IPEDSCell
THECBCell = namedtuple('THECBCell', 'long_name, year, year_type')


def parse_header_cell(text):
    """Get details needed for THECBCell out of the text."""
    search = re.match(r'(.+)\s\((\w+)\s(\d{4})\)', text)
    if search:
        name, year_type_raw, year_raw = search.groups()
        return THECBCell(name, int(year_raw), year_type_raw.lower())
    return text


def top_10_percent(path):
    from tx_highered.models import Admissions as Model

    year_type = "fall"

    report = reader(open(path))
    original_header = report.next()
    header = map(parse_header_cell, original_header)
    print header

    for row in report:
        print row
    return
    doc = etree.parse(path)
    rows = doc.xpath('//tr')
    header = [x.text_content() for x in rows[1]]
    for row in rows[2:]:
        fice_id = row[1].text
        if not fice_id:
            continue
        inst = Institution.objects.get(fice_id=fice_id)
        print "top 10 percent: %s" % inst.name
        for i, col in enumerate(row[2:], 2):
            value = col.text.strip().lower()
            if value == "":
                value = None
            elif value == "n/a" or value == "na":
                value = None
            else:
                value = value.rstrip("%")
            year = get_year(header[i])
            report, _ = Model.objects.get_or_create(institution=inst, year=year,
                defaults=dict(year_type=year_type))
            report.percent_top10rule = value
            report.save()


report = sys.argv[-2]
path = sys.argv[-1]

if len(sys.argv) == 2:
    # no report given, guess it
    report = os.path.splitext(os.path.basename(sys.argv[1]))[0]


if report == 'top_10_percent':
    top_10_percent(path)
