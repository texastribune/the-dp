"""
Import the list of current public institutions
source: http://www.txhighereddata.org/Interactive/Institutions.cfm

"""
import urllib2

from django.template.defaultfilters import slugify
from lxml import html as etree

from thedp.models import Institution, System

# CONFIGURATION
SOURCE = "http://www.txhighereddata.org/Interactive/Institutionsshow_Excel.cfm?All=1"

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


def normalize_keys(data, mapping=[]):
    for key in data.keys():
        if key in mapping:
            value = data.pop(key)
            data[mapping[key]] = value


def main():
    r = urllib2.urlopen(SOURCE)
    doc = etree.parse(r)
    rows = doc.xpath('//tr')

    headings = [x.text_content().strip() for x in rows[0].getchildren()]
    for row in rows[1:]:
        data = dict(zip(headings, [x.text_content().strip() for x in row.getchildren()]))
        normalize_keys(data, mapping=I_MAP)
        if not data['name']:
            continue
        data.pop('TODO')
        slug = slugify(data['name'])
        system_name = data.pop('system__name')
        if system_name:
            system, _ = System.objects.get_or_create(slug=slugify(system_name), name=system_name)
        else:
            system = None
        data['system'] = system
        i, c = Institution.objects.get_or_create(slug=slug, defaults=data)
        print i, c


if __name__ == "__main__":
    main()
