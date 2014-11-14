"""
Import IPEDS Custom Reports.

Usage:
  ./import_customreport <csv1> <csv2> ...
"""
from collections import namedtuple
import logging
import os
import sys

from tx_highered.ipeds_csv_reader import IpedsCSVReader
from tx_highered.models import (
    Institution, Admissions, PriceTrends, TestScores, Enrollment,
    GraduationRates,
)


# This tells the importer how to interpret IPEDS short variables for import
# into a Django model and field
ReportDatum = namedtuple('ReportDatum', ['model', 'field', 'year_type'])
FIELD_MAPPINGS = {
    'ADMSSN': ReportDatum(Admissions, 'number_admitted', 'fall'),
    'APPLCN': ReportDatum(Admissions, 'number_of_applicants', 'fall'),
    'ENRLT': ReportDatum(Admissions, 'number_admitted_who_enrolled', 'fall'),
    # Price Trends
    'chg2ay3': ReportDatum(PriceTrends, 'tuition_fees_in_state', 'fall'),
    'chg3ay3': ReportDatum(PriceTrends, 'tuition_fees_outof_state', 'fall'),
    'chg4ay3': ReportDatum(PriceTrends, 'books_and_supplies', 'fall'),
    'chg5ay3': ReportDatum(PriceTrends, 'room_and_board_on_campus', 'fall'),

    # Test Scores
    'SATNUM': ReportDatum(TestScores, 'sat_submitted_number', 'fall'),
    'SATPCT': ReportDatum(TestScores, 'sat_submitted_percent', 'fall'),
    'ACTNUM': ReportDatum(TestScores, 'act_submitted_number', 'fall'),
    'ACTPCT': ReportDatum(TestScores, 'act_submitted_percent', 'fall'),
    'SATVR25': ReportDatum(TestScores, 'sat_verbal_25th_percentile', 'fall'),
    'SATVR75': ReportDatum(TestScores, 'sat_verbal_75th_percentile', 'fall'),
    'SATMT25': ReportDatum(TestScores, 'sat_math_25th_percentile', 'fall'),
    'SATMT75': ReportDatum(TestScores, 'sat_math_75th_percentile', 'fall'),
    'SATWR25': ReportDatum(TestScores, 'sat_writing_25th_percentile', 'fall'),
    'SATWR75': ReportDatum(TestScores, 'sat_writing_75th_percentile', 'fall'),
    'ACTCM25': ReportDatum(TestScores, 'act_composite_25th_percentile', 'fall'),
    'ACTCM75': ReportDatum(TestScores, 'act_composite_75th_percentile', 'fall'),
    'ACTEN25': ReportDatum(TestScores, 'act_english_25th_percentile', 'fall'),
    'ACTEN75': ReportDatum(TestScores, 'act_english_75th_percentile', 'fall'),
    'ACTMT25': ReportDatum(TestScores, 'act_math_25th_percentile', 'fall'),
    'ACTMT75': ReportDatum(TestScores, 'act_math_75th_percentile', 'fall'),
    'ACTWR25': ReportDatum(TestScores, 'act_writing_25th_percentile', 'fall'),
    'ACTWR75': ReportDatum(TestScores, 'act_writing_75th_percentile', 'fall'),

    # Enrollment
    'PctEnrWh': ReportDatum(Enrollment, 'total_percent_white', 'fall'),
    'PctEnrBK': ReportDatum(Enrollment, 'total_percent_black', 'fall'),
    'PctEnrHS': ReportDatum(Enrollment, 'total_percent_hispanic', 'fall'),
    'PctEnrAP': ReportDatum(Enrollment, 'total_percent_asian', 'fall'),
    'PctEnrAN': ReportDatum(Enrollment, 'total_percent_native', 'fall'),
    'PctEnrUn': ReportDatum(Enrollment, 'total_percent_unknown', 'fall'),
    'ENRTOT': ReportDatum(Enrollment, 'total', 'fall'),
    'FTE': ReportDatum(Enrollment, 'fulltime_equivalent', 'fall'),
    'EnrFt': ReportDatum(Enrollment, 'fulltime', 'fall'),
    'EnrPt': ReportDatum(Enrollment, 'parttime', 'fall'),

    # GraduationRates
    'GBA4RTT': ReportDatum(GraduationRates, 'bachelor_4yr', 'aug'),
    'GBA5RTT': ReportDatum(GraduationRates, 'bachelor_5yr', 'aug'),
    'GBA6RTT': ReportDatum(GraduationRates, 'bachelor_6yr', 'aug'),
}


def generic(path):
    """Read the CSV and import into the appropriate model."""
    logger = logging.getLogger(__name__)
    reader = IpedsCSVReader(open(path, 'rb'))
    for row in reader:
        unit_id, ipeds_id = row[0]
        assert unit_id == 'UnitID'
        try:
            institution = Institution.objects.get(ipeds_id=ipeds_id)
        except Institution.MultipleObjectsReturned:
            logger.critical('DUPLICATE IPEDS: {}'.format(ipeds_id))
            sys.exit()
        except Institution.DoesNotExist:
            # TODO echo the name too
            logger.error('MISSING Institution: {}'.format(ipeds_id))
            continue
        for key, value in row[2:]:
            logger.debug(u'{} {}'.format(key, value))
            if key is None or value is '':
                # skip cells with no data, CSVs will give empty strings for
                # missing values
                continue
            try:
                finder = FIELD_MAPPINGS[key.short_name]
            except KeyError:
                logger.error('MISSING: cannot interpret {}'
                    .format(key.short_name))
                continue
            defaults = {
                finder.field: value,
                'year_type': finder.year_type,
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
                .format(instance, key.short_name, logging_state))


if __name__ == '__main__':
    for path in sys.argv[1:]:
        if os.path.isfile(path):
            generic(path)
