"""

Sample CSV structure:
UnitID,Institution Name,CINSON(DRVIC2011),COTSON(DRVIC2011),CINSON(DRVIC2010_RV),COTSON(DRVIC2010_RV),CINSON(DRVIC2009_RV),COTSON(DRVIC2009_RV),CINSON(DRVIC2008),COTSON(DRVIC2008),CINSON(DRVIC2007),COTSON(DRVIC2007),CINSON(DRVIC2006),COTSON(DRVIC2006),CINSON(IC2005_AY),COTSON(IC2005_AY),chg1ay3(IC2005_AY),chg2ay3(IC2005_AY),chg3ay3(IC2005_AY),chg4ay3(IC2005_AY),chg5ay3(IC2005_AY),chg7ay3(IC2005_AY),chg9ay3(IC2005_AY),CINSON(IC2004_AY),COTSON(IC2004_AY),chg1ay3(IC2004_AY),chg2ay3(IC2004_AY),chg3ay3(IC2004_AY),chg4ay3(IC2004_AY),chg5ay3(IC2004_AY),chg7ay3(IC2004_AY),chg9ay3(IC2004_AY),CINSON(IC2003_AY),COTSON(IC2003_AY),chg1ay3(IC2003_AY),chg2ay3(IC2003_AY),chg3ay3(IC2003_AY),chg4ay3(IC2003_AY),chg5ay3(IC2003_AY),chg7ay3(IC2003_AY),chg9ay3(IC2003_AY),chg1ay3(IC2011_AY),chg2ay3(IC2011_AY),chg3ay3(IC2011_AY),chg4ay3(IC2011_AY),chg5ay3(IC2011_AY),chg7ay3(IC2011_AY),chg9ay3(IC2011_AY),chg1ay3(IC2010_AY_RV),chg2ay3(IC2010_AY_RV),chg3ay3(IC2010_AY_RV),chg4ay3(IC2010_AY_RV),chg5ay3(IC2010_AY_RV),chg7ay3(IC2010_AY_RV),chg9ay3(IC2010_AY_RV),chg1ay3(IC2009_AY_RV),chg2ay3(IC2009_AY_RV),chg3ay3(IC2009_AY_RV),chg4ay3(IC2009_AY_RV),chg5ay3(IC2009_AY_RV),chg7ay3(IC2009_AY_RV),chg9ay3(IC2009_AY_RV),chg1ay3(IC2008_AY),chg2ay3(IC2008_AY),chg3ay3(IC2008_AY),chg4ay3(IC2008_AY),chg5ay3(IC2008_AY),chg7ay3(IC2008_AY),chg9ay3(IC2008_AY),chg1ay3(IC2007_AY),chg2ay3(IC2007_AY),chg3ay3(IC2007_AY),chg4ay3(IC2007_AY),chg5ay3(IC2007_AY),chg7ay3(IC2007_AY),chg9ay3(IC2007_AY),chg1ay3(IC2006_AY),chg2ay3(IC2006_AY),chg3ay3(IC2006_AY),chg4ay3(IC2006_AY),chg5ay3(IC2006_AY),chg7ay3(IC2006_AY),chg9ay3(IC2006_AY),chg1ay3(IC2002_AY),chg2ay3(IC2002_AY),chg3ay3(IC2002_AY),chg4ay3(IC2002_AY),chg5ay3(IC2002_AY),chg7ay3(IC2002_AY),chg9ay3(IC2002_AY),chg1ay3(IC2001_AY),chg2ay3(IC2001_AY),chg3ay3(IC2001_AY),chg4ay3(IC2001_AY),chg5ay3(IC2001_AY),chg7ay3(IC2001_AY),chg9ay3(IC2001_AY),chg1ay3(IC2000_AY),chg2ay3(IC2000_AY),chg3ay3(IC2000_AY),chg4ay3(IC2000_AY),chg5ay3(IC2000_AY),chg7ay3(IC2000_AY),chg9ay3(IC2000_AY),
222178,Abilene Christian University,38250,38250,35300,35300,32300,32300,30500,30500,27950,27950,26502,26502,24475,24475,14610,14610,14610,1195,5670,,,23420,23420,14200,14200,14200,1000,5270,5270,2950,22050,22050,13290,13290,13290,800,5080,5080,2880,25270,25270,25270,1250,8316,,,22760,22760,22760,1250,7884,,,20290,20290,20290,1200,7510,,,18930,18930,18930,1150,7236,,,17410,17410,17410,1100,6350,,,16330,16330,16330,1050,6120,,,12430,12430,12430,560,4830,4830,2830,11650,11650,11650,540,4650,4650,2800,10910,10910,10910,540,4420,4420,2730,

"""

import os
import sys

from ipeds_importer.utils import IpedsCsvReader

from tx_highered.models import Institution


PRIMARY_MAPPING = ('UnitID', 'ipeds_id')


def prices(path):
    from tx_highered.models import PriceTrends
    # configuration
    FIELD_MAPPING = (
        ('chg2ay3', 'tuition_fees_in_state'),
        ('chg3ay3', 'tuition_fees_outof_state'),
        ('chg4ay3', 'books_and_supplies'))
    PRIMARY_MAPPING = ('UnitID', 'ipeds_id')
    YEAR_TYPE = 'fall'
    reader = IpedsCsvReader(open(path, "rb"), field_mapping=FIELD_MAPPING,
                            primary_mapping=PRIMARY_MAPPING, year_type=YEAR_TYPE)
    # reader.explain_header()
    reader.parse_rows(institution_model=Institution, report_model=PriceTrends)


def testscores(path):
    from tx_highered.models import TestScores
    # configuration
    FIELD_MAPPING = (
        ('SATNUM', 'sat_submitted_number'),
        ('SATPCT', 'sat_submitted_percent'),
        ('ACTNUM', 'act_submitted_number'),
        ('ACTPCT', 'act_submitted_percent'),
        ('SATVR25', 'sat_verbal_25th_percentile'),
        ('SATVR75', 'sat_verbal_75th_percentile'),
        ('SATMT25', 'sat_math_25th_percentile'),
        ('SATMT75', 'sat_math_75th_percentile'),
        ('SATWR25', 'sat_writing_25th_percentile'),
        ('SATWR75', 'sat_writing_75th_percentile'),
        ('ACTCM25', 'act_composite_25th_percentile'),
        ('ACTCM75', 'act_composite_75th_percentile'),
        ('ACTEN25', 'act_english_25th_percentile'),
        ('ACTEN75', 'act_english_75th_percentile'),
        ('ACTMT25', 'act_math_25th_percentile'),
        ('ACTMT75', 'act_math_75th_percentile'),
        ('ACTWR25', 'act_writing_25th_percentile'),
        ('ACTWR75', 'act_writing_75th_percentile'))
    PRIMARY_MAPPING = ('UnitID', 'ipeds_id')
    YEAR_TYPE = 'fall'
    reader = IpedsCsvReader(open(path, "rb"), field_mapping=FIELD_MAPPING,
                            primary_mapping=PRIMARY_MAPPING, year_type=YEAR_TYPE)
    reader.parse_rows(institution_model=Institution, report_model=TestScores)


def enrollment(path):
    from tx_highered.models import Enrollment
    # configuration
    FIELD_MAPPING = (
        ('PctEnrWh', 'total_percent_white'),
        ('PctEnrBK', 'total_percent_black'),
        ('PctEnrHS', 'total_percent_hispanic'),
        ('PctEnrAP', 'total_percent_asian'),
        ('PctEnrAN', 'total_percent_native'),
        ('PctEnrUn', 'total_percent_unknown'),
        ('ENRTOT', 'total'),
        ('FTE', 'fulltime_equivalent'),
        ('EnrFt', 'fulltime'),
        ('EnrPt', 'parttime'))
    PRIMARY_MAPPING = ('UnitID', 'ipeds_id')
    YEAR_TYPE = 'fall'
    reader = IpedsCsvReader(open(path, "rb"), field_mapping=FIELD_MAPPING,
                            primary_mapping=PRIMARY_MAPPING, year_type=YEAR_TYPE)
    reader.parse_rows(institution_model=Institution, report_model=Enrollment)


def graduation_rates(path):
    from tx_highered.models import GraduationRates as report_model
    field_mapping = (
        ('GBA4RTT', 'bachelor_4yr'),
        ('GBA5RTT', 'bachelor_5yr'),
        ('GBA6RTT', 'bachelor_6yr'))
    year_type = 'aug'
    reader = IpedsCsvReader(open(path, "rb"), field_mapping=field_mapping,
                            primary_mapping=PRIMARY_MAPPING, year_type=year_type)
    reader.parse_rows(institution_model=Institution, report_model=report_model)


report = sys.argv[-2]
path = sys.argv[-1]

if len(sys.argv) == 2:
    # no report given, guess it
    report = os.path.splitext(os.path.basename(sys.argv[1]))[0]

if report == 'prices':
    prices(path)
elif report == 'testscores':
    testscores(path)
elif report == 'enrollment':
    enrollment(path)
elif report == 'grad_rates':
    graduation_rates(path)
else:
    reader = IpedsCsvReader(open(path, "rb"))
    reader.explain_header()
