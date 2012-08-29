from pyquery import PyQuery as pq
import requests

REPORT_URL = "http://reports.thecb.state.tx.us/ibi_apps/WFServlet?"

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
    institutions = []

    category_data = CATEGORY_DATA[category]
    payload = generate_payload(category_data)
    response = requests.get(REPORT_URL, params=payload)
    doc = pq(response.content)

    current_data = {}
    current_year = None
    current_name = None
    for tr in doc.find('tr'):
        name = None
        fice = None
        current_year = 2011
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
                        import pprint
                        pprint.pprint(institutions[-1])
                    current_data = {}
                    current_name = name
            elif td_class in FICE_CLASSES:
                fice = td.text.strip()
            elif td_class in ETHNICITY_CLASSES:
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


def clean_institution(institution):
    pass


if __name__ == '__main__':
    get_institutions('public')
    get_institutions('public 2-year')
