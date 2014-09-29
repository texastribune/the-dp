#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Import from the Accountability report system.

Usage:
    ./import_thecb_report.py CSV1 CSV2 ...

Modeled after import_customreport.py, but written lazier.
"""
from collections import namedtuple
from csv import reader
import logging
import os
import re
import sys

from tx_highered.models import Institution, Admissions


logger = logging.getLogger(__name__)

# Similar to IPEDSCell
THECBCell = namedtuple('THECBCell', 'long_name, year, year_type')

ReportDatum = namedtuple('ReportDatum', ['model', 'field'])
FIELD_MAPPINGS = {
    u'First-Time Students in Top 10% (Percent)':
    ReportDatum(Admissions, 'percent_top10rule'),
}
# based on reports.YearBasedInstitutionStatsModel.YEAR_TYPE_CHOICES
YEAR_TYPES = {
    'Fall': 'fall',
    'FY': 'fiscal',
    # academic
    # calendar
    # aug
}


def parse_header_cell(text):
    """Get details needed for THECBCell out of the text."""
    search = re.match(r'(.+)\((\w+)\s(\d{4})\)', text)
    if search:
        name_raw, year_type_raw, year_raw = search.groups()
        year_type = YEAR_TYPES[year_type_raw]
        return THECBCell(name_raw.strip(), int(year_raw), year_type)
    return text


def generic(path):
    report = reader(open(path))
    original_header = report.next()
    header = map(parse_header_cell, original_header)
    print header

    for row in report:
        data = zip(header, row)
        fice_id = row[1]
        institution = Institution.objects.get(fice_id=fice_id)
        for key, value in data[3:]:
            if value.upper() in ('', 'NA'):
                # HACK so bad values get stored as NULL. NULl means we tried to
                # get data but got nothing or bad data.
                value = None
            logger.debug(u'{} {}'.format(key, value))
            try:
                finder = FIELD_MAPPINGS[key.long_name]
            except KeyError:
                logger.error('MISSING: cannot interpret {}'
                    .format(key.long_name))
                continue
            defaults = {
                finder.field: value,
                'year_type': key.year_type,
            }
            logging_state = 'CREATED'
            instance, created = finder.model.objects.get_or_create(
                institution=institution, year=key.year,
                defaults=defaults)
            if not created:
                if unicode(getattr(instance, finder.field)) != value:
                    logging_state = 'UPDATED'
                    instance.__dict__.update(defaults)
                    instance.save()
                else:
                    logging_state = 'SKIP'
            logger.info(u'{} {} {}'
                .format(instance, key.long_name, logging_state))


if __name__ == '__main__':
    for path in sys.argv[1:]:
        if os.path.isfile(path):
            generic(path)
