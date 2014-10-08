"""
Usage:

    python load_enrollment.py

Loads enrollment data from THECB's PREP online site:
http://reports.thecb.state.tx.us/approot/dwprodrpt/enrmenu.htm

NOTE: the total enrollment number is not a meaningful figure except for
boasting purposes. The full time equivalent figure is a better measure of
student population, which comes from the Accountability system, not PREP.
"""
from collections import defaultdict
import logging

from pyquery import PyQuery as pq
import requests

from tx_highered.models import Institution, PublicEnrollment
from tx_highered.thecb_importer.utils import create_or_update


REPORT_URL = "http://reports.thecb.state.tx.us/ibi_apps/WFServlet?"

CURRENT_YEAR = 2014  # TODO pull the current year directly from the data

CATEGORY_DATA = {
    'public': {
        'instcateg': 'Public University',
    },
    'public 2-year': {
        'instcateg': 'Public 2-Year College',
    },
}

NAME_CLASSES = ['x10_0', 'x10_1']
FICE_CLASSES = ['x11_0', 'x11_1']
ETHNICITY_CLASSES = ['x12_0', 'x12_1']
DATA_CLASSES = ['x13_0', 'x13_1', 'x14_0', 'x14_1']
KNOWN_CLASSES = NAME_CLASSES + FICE_CLASSES + ETHNICITY_CLASSES + DATA_CLASSES

TOTAL_CLASS = 'x15'
KNOWN_CLASSES.append(TOTAL_CLASS)


logger = logging.getLogger(__name__)


def generate_payload(extra_data):
    return dict({
        'IBIC_server': 'EDASERVE',
        'IBIF_ex': 'enrethnicinst',
        'HIGHER_ED_RPT_SEM_NAME': 'Fall',
        'HIGHER_ED_RPT_YEAR': 'FOC_NONE',
        'instcode': 'FOC_NONE',
        'WFFMT': 'HTML',
        'IBIMR_Random': '0.9490816127508879',
        'instname': 'FOC_NONE',
    }, **extra_data)


def get_institutions(category):
    logger.debug('get_institutions - {}'.format(category))
    institutions = []

    category_data = CATEGORY_DATA[category]
    payload = generate_payload(category_data)
    response = requests.get(REPORT_URL, params=payload)
    doc = pq(response.content)

    current_data = {}
    fice = None
    current_year = None
    current_name = None
    for tr in doc.find('tr'):
        name = None
        current_year = CURRENT_YEAR
        for td in tr.getchildren():
            td_class = td.attrib.get('class')
            if td_class not in KNOWN_CLASSES or 'colspan' in td.attrib:
                continue

            if td_class in NAME_CLASSES:
                name = td.text.strip()
                if name and name != current_name:
                    if current_name:
                        institutions.append({
                            'name': current_name,
                            'fice': fice or None,
                            'data': current_data
                        })
                    current_data = {}
                    current_name = name
            elif td_class in FICE_CLASSES:
                if td.text.strip():
                    fice = td.text.strip()
            elif td_class in ETHNICITY_CLASSES:
                if td.text.strip():
                    ethnicity = td.text.strip()
            elif td_class == TOTAL_CLASS:
                current_data.setdefault('total', {})
                current_data['total'][current_year] = td.text.strip()
                current_year = current_year - 1
            else:
                current_data.setdefault(ethnicity, {})
                current_data[ethnicity][current_year] = td.text.strip()
                current_year = current_year - 1

    return institutions


def clean_field_name(field):
    return {
        'African American': 'african_american_count',
        'American Indian/Alaskan Native': 'native_american_count',
        'Asian': 'asian_count',
        'Hispanic': 'hispanic_count',
        'International': 'international_count',
        'Multiracial': 'multiracial_count',
        'Native Hawaiian/Pacific Island': 'pacific_islander_count',
        'Unknown or Not Reported': 'unknown_count',
        'White': 'white_count',
        'total': 'total'
    }[field]


def clean_institution_data(data):
    # Look up related institution from the FICE ID
    try:
        institution = Institution.objects.get(fice_id=data['fice'])
    except Institution.DoesNotExist:
        logger.warn('missing FICE ID %(fice)s (%(name)s)\n' % data)
        return

    # The data item looks like this (multiple ethnicities with a total):
    # { race: [{year: enrollment}, ...], ..., total: [...] }
    data_by_year = defaultdict(dict)
    for field, value in data['data'].items():
        field_name = clean_field_name(field)
        for year, enrollment in value.items():
            data_by_year[year][field_name] = int(enrollment.replace(',', ''))

    # Calculate percentages
    for year, year_data in data_by_year.items():
        total = year_data['total']
        if total != 0:
            for field, count in year_data.items():
                if field == 'total':
                    continue
                percent_field = field.replace('_count', '_percent')
                year_data[percent_field] = round(100.0 * count / total, 1)
        yield dict(year_data, institution=institution, year=year)


def main():
    for category in ('public', 'public 2-year'):
        for institution in get_institutions(category):
            for cleaned_data in clean_institution_data(institution):
                inst = cleaned_data.pop('institution')
                year = cleaned_data.pop('year')
                logger.info('Instutition: {}, Year: {}'.format(inst, year))
                logger.debug('data: {}'.format(cleaned_data))
                create_or_update(PublicEnrollment.objects, institution=inst,
                    year=year, defaults=cleaned_data)


if __name__ == '__main__':
    main()
