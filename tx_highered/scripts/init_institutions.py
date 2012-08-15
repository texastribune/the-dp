"""
Import the list of current public institutions
source: http://www.txhighereddata.org/Interactive/Institutions.cfm

"""
import urllib2

from django.template.defaultfilters import slugify

from tx_highered.models import Institution, System
from . import utils

# CONFIGURATION
SOURCE = "http://www.txhighereddata.org/Interactive/Institutionsshow_Excel.cfm?All=1"
INSTITUTION_TYPES = (
    ("pub_u", "http://www.txhighereddata.org/Interactive/InstitutionsShow_Excel.cfm?Level=1&Type=1"),
    ("pub_cc", "http://www.txhighereddata.org/Interactive/InstitutionsShow_Excel.cfm?Level=2&Type=1"),
    ("pub_med", "http://www.txhighereddata.org/Interactive/InstitutionsShow_Excel.cfm?Level=3&Type=1"),
    ("pub_tech", "http://www.txhighereddata.org/Interactive/InstitutionsShow_Excel.cfm?Level=7&Type=1"),
    ("pub_state", "http://www.txhighereddata.org/Interactive/InstitutionsShow_Excel.cfm?Level=11&Type=1"),
    ("pri_u", "http://www.txhighereddata.org/Interactive/InstitutionsShow_Excel.cfm?Level=1&Type=2"),
    ("pri_jr", "http://www.txhighereddata.org/Interactive/InstitutionsShow_Excel.cfm?Level=9&Type=2"),
    ("pri_med", "http://www.txhighereddata.org/Interactive/InstitutionsShow_Excel.cfm?Level=3&Type=2"),
    ("pri_chi", "http://www.txhighereddata.org/Interactive/InstitutionsShow_Excel.cfm?Level=10&Type=2"),
)


# institution header to fieldname map
I_MAP = {'Institution Name': 'name',
         'System Name': 'system__name',
         'Address': 'address',
         'City': 'city',
         'Zip Code': 'zip_code',
         'Administrative Officer': 'TODO',
         'Administrative Officer Title': 'TODO',
         'MainTelephone': 'phone',
         'Website Address': 'url'}


def pull(institution_type, source):
    r = urllib2.urlopen(source)
    reader = utils.DictReader(r, mapping=I_MAP)

    for data in reader:
        if not data['name']:
            continue
        data.pop('TODO')
        slug = slugify(data['name'])
        data['institution_type'] = institution_type
        system_name = data.pop('system__name')
        if system_name:
            system, _ = System.objects.get_or_create(slug=slugify(system_name), name=system_name)
        else:
            system = None
        data['system'] = system
        i, c = Institution.objects.get_or_create(slug=slug, defaults=data)
        print i, c


def main():
    for t, url in INSTITUTION_TYPES:
        pull(t, url)


if __name__ == "__main__":
    main()
