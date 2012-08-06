"""
Import from the Accountability report system

"""
import os
import re
import sys

from lxml import html as etree

from tx_highered.models import Institution


def get_year(s):
    search = re.search("\d{4}", s)
    if search:
        return search.group()
    return None


def top_10_percent(path):
    from tx_highered.models import Admissions as Model

    year_type = "fall"

    doc = etree.parse(path)
    rows = doc.xpath('//tr')
    header = [x.text_content() for x in rows[1]]
    for row in rows[2:]:
        fice_id = row[1].text
        if not fice_id:
            continue
        inst = Institution.objects.get(fice_id=fice_id)
        print inst
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
            report.percent_of_applicants_top10rule = value
            report.save()


report = sys.argv[-2]
path = sys.argv[-1]

if len(sys.argv) == 2:
    # no report given, guess it
    report = os.path.splitext(os.path.basename(sys.argv[1]))[0]


if report == 'top_10_percent':
    top_10_percent(path)