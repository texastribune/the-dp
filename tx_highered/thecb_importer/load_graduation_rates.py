#! /usr/bin/env python
import re
import sys
from collections import defaultdict

from lxml import html as etree

from tx_highered.models import Institution
from tx_highered.models import PublicGraduationRates


def parse_year(s):
    search = re.search("\d{4}", s)
    if search:
        return search.group()

    return None


def parse_header(header):
    year = parse_year(header)
    prefix, suffix = None, None

    # Parse degree prefix
    if 'Associate' in header:
        prefix = 'associate'
    else:
        prefix = 'bachelor'

    # Parse year suffix
    if 'Three-Year' in header:
        suffix = '3yr'
    elif 'Four-Year' in header:
        suffix = '4yr'
    elif 'Five-Year' in header:
        suffix = '5yr'
    elif 'Six-Year' in header:
        suffix = '6yr'

    # Combine prefix and suffix into field name
    if prefix and suffix:
        return '%s_%s' % (prefix, suffix), year
    else:
        return None, None


def parse_html(path):
    html = etree.parse(path)
    row_iter = iter(html.xpath('//tr'))
    # Throw away the report header in the first row
    first_row = next(row_iter)
    if len(first_row.getchildren()) == 1:
        first_row = next(row_iter)
    # The column names are in the second row
    headers = [col.text_content() for col in first_row]
    data = []
    for row in row_iter:
        values = [c.text.strip().strip('%') if c.text else None for c in row]
        values = [v if v != 'N/A' else None for v in values]
        record = dict(zip(headers, values))
        data.append(record)

    return data


def load_graduation_rates(path):
    data = parse_html(path)
    obj_data_by_institution_year = defaultdict(dict)
    for row in data:
        row.pop('Institution')
        fice_id = row.pop('FICE')
        if not fice_id:
            continue
        else:
            fice_id = fice_id.split(' (')[0]
        try:
            institution = Institution.objects.get(fice_id=fice_id)
        except Institution.DoesNotExist:
            continue
        for key, value in row.items():
            field, year = parse_header(key)
            if not field:
                continue

            # Set the field value for this institution for this year
            obj_key = '%s:%s' % (fice_id, year)
            obj_data = obj_data_by_institution_year[obj_key]
            obj_data.setdefault('institution', institution)
            obj_data.setdefault('year', year)
            obj_data.setdefault('year_type', 'fiscal')
            obj_data[field] = value

    # Save the graduation rates
    for obj_data in obj_data_by_institution_year.itervalues():
        print obj_data['institution']
        PublicGraduationRates.objects.create(**obj_data)


if __name__ == '__main__':
    load_graduation_rates(sys.argv[1])
