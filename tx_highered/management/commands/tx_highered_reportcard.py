# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.models import Model, Q

from tx_highered.models import Institution


class Command(BaseCommand):
    help = (
        'Create a report card of our data quality. Run it through '
        'http://setosa.io/csv-fingerprint/ for a quick visualization.'
    )
    option_list = BaseCommand.option_list + (
        make_option('--year',
            dest='year',
            type='int',
            help='Data must be from at least this year'),
    )

    def handle(self, *args, **options):

        def latest_year(model_or_queryset, relation=None):
            """Latest year institution has data, returns year or ''."""
            if relation is not None and isinstance(model_or_queryset, Model):
                queryset = getattr(model_or_queryset, relation).all()
            else:
                queryset = model_or_queryset
            try:
                year = queryset.order_by('-year')[0].year
                if options['year'] is not None and year < options['year']:
                    return ''
                else:
                    return year
            except IndexError:
                return ''

        header = (
            'slug',
            'type',
            'Admissions IPEDS',
            'Admissions THECB',
            'Test Scores',
            'Full-Time Equivalent',
            'Demographics IPEDS',
            'Demographics THECB',
            'Price Trends',
            'Graduation IPEDS',
            'Graduation THECB',
        )
        print ','.join(header)
        institutions = (Institution.objects.published()
            .order_by('institution_type', 'is_private', 'name'))
        for institution in institutions:
            row = [institution.slug, institution.institution_type]
            row.append(latest_year(institution, 'admissions'))
            if institution.is_private:
                row.append('NA')
            else:
                row.append(latest_year(institution, 'publicadmissions'))

            row.append(latest_year(institution, 'testscores'))

            # Enrollment
            #
            # We only care about fulltime equivalent, which is only in IPEDS
            # for now.
            row.append(latest_year(institution.enrollment.filter(
                fulltime_equivalent__isnull=False)))

            # Demographics
            #
            # Assume that every school at least has white or black students
            row.append(latest_year(institution.enrollment.filter(
                Q(total_percent_white__isnull=False) |
                Q(total_percent_black__isnull=False)
            )))
            if institution.is_private:
                row.append('NA')
            else:
                row.append(latest_year(institution.publicenrollment.filter(
                    Q(white_percent__isnull=False) |
                    Q(african_american_percent=False)
                )))

            row.append(latest_year(institution, 'pricetrends'))

            # Bachelor Degree Graduation Rates
            #
            # We currently only care about bachelor's degrees, but will
            # hopefully update the codebase to display associates degrees too.
            row.append(latest_year(institution.graduationrates.filter(
                Q(bachelor_4yr__isnull=False) |
                Q(bachelor_6yr__isnull=False),
            )))
            if institution.is_private:
                row.append('NA')
            else:
                row.append(latest_year(institution.publicgraduationrates.filter(
                    Q(bachelor_4yr__isnull=False) |
                    Q(bachelor_6yr__isnull=False),
                )))

            print ','.join(map(unicode, row))
