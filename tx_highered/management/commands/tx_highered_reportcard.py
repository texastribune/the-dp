# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db.models import Model, Q

from tx_highered.models import Institution


class Command(BaseCommand):
    help = (
        'Create a report card of our data quality. Run it through '
        'http://setosa.io/csv-fingerprint/ for a quick visualization.'
    )

    def handle(self, *args, **options):

        def latest_year(model_or_queryset, relation=None):
            """Latest year institution has data, returns year or ''."""
            if relation is not None and isinstance(model_or_queryset, Model):
                queryset = getattr(model_or_queryset, relation).all()
            else:
                queryset = model_or_queryset
            try:
                return queryset.order_by('-year')[0].year
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

            # Enrollment
            #
            # We only care about fulltime equivalent, which is only in IPEDS
            # for now.
            header.append('Full-Time Equivalent')
            row.append(latest_year(institution.enrollment.filter(
                fulltime_equivalent__isnull=False)))

            # Demographics
            #
            # Assume that every school at least has white or black students
            header.append('Demographics IPEDS')
            row.append(latest_year(institution.enrollment.filter(
                Q(total_percent_white__isnull=False) |
                Q(total_percent_black__isnull=False)
            )))
            header.append('Demographics THECB')
            if institution.is_private:
                row.append('NA')
            else:
                row.append(latest_year(institution.publicenrollment.filter(
                    Q(white_percent__isnull=False) |
                    Q(african_american_percent=False)
                )))

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
