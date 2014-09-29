#! /usr/bin/env python
"""
Import from the Accountability report system

TODO what is this for? How come this only does top 10 percent?
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


def parse_header_cell(text):
    """Get details needed for THECBCell out of the text."""
    search = re.match(r'(.+)\s\((\w+)\s(\d{4})\)', text)
    if search:
        name, year_type_raw, year_raw = search.groups()
        year_type = year_type_raw.lower()
        # based on reports.YearBasedInstitutionStatsModel.YEAR_TYPE_CHOICES
        assert year_type in (
            'academic',
            'calendar',
            'fall',
            'fiscal',
            'aug',
        )
        return THECBCell(name, int(year_raw), year_type)
    return text


def top_10_percent(path):
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


report = sys.argv[-2]
path = sys.argv[-1]

if len(sys.argv) == 2:
    # no report given, guess it
    report = os.path.splitext(os.path.basename(sys.argv[1]))[0]


if report == 'top_10_percent':
    top_10_percent(path)
