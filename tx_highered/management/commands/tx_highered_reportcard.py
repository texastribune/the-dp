# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from tx_highered.models import Institution


class Command(BaseCommand):
    help = (
        'Create a report card of our data quality. Run it through '
        'http://setosa.io/csv-fingerprint/ for a quick visualization.'
    )

    def handle(self, *args, **options):

        def latest_year(institution, relation):
            """Latest year institution has data, returns year or ''."""
            try:
                return getattr(institution, relation).all().order_by('-year')[0].year
            except IndexError:
                return ''

        header = ['name']
        print ','.join(header)
        for institution in Institution.objects.published():
            row = [institution.slug]
            header.append('Admissions IPEDS')
            row.append(latest_year(institution, 'admissions'))
            header.append('Admissions THECB')
            if institution.is_private:
                row.append('NA')
            else:
                row.append(latest_year(institution, 'publicadmissions'))

            header.append('Test Scores')
            row.append(latest_year(institution, 'testscores'))

            header.append('Enrollment IPEDS')
            row.append(latest_year(institution, 'enrollment'))
            header.append('Enrollment THECB')
            if institution.is_private:
                row.append('NA')
            else:
                row.append(latest_year(institution, 'publicenrollment'))

            header.append('Price Trends')
            row.append(latest_year(institution, 'pricetrends'))

            header.append('Graduation IPEDS')
            row.append(latest_year(institution, 'graduationrates'))
            header.append('Graduation THECB')
            if institution.is_private:
                row.append('NA')
            else:
                row.append(latest_year(institution, 'publicgraduationrates'))

            print ','.join(map(unicode, row))

        # print header
        # print rows
