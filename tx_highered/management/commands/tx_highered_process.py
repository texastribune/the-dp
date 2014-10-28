# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from tx_highered.models import Admissions


class Command(BaseCommand):
    help = 'Post-process data higher ed data. Safe to run multiple times.'

    def handle(self, *args, **options):
        # Backfill missing `percent_of_applicants_admitted`
        for x in Admissions.objects.filter(percent_of_applicants_admitted=None, number_of_applicants__gt=0, number_admitted__gt=0):
            x.percent_of_applicants_admitted = \
                x.number_admitted * 1000 / x.number_of_applicants / 10.0
            print x, '% admitted', x.percent_of_applicants_admitted
            x.save()

        # Backfill missing `percent_of_admitted_who_enrolled`
        for x in Admissions.objects.filter(percent_of_admitted_who_enrolled__isnull=True, number_admitted_who_enrolled__gt=0, number_admitted__gt=0):
            x.percent_of_admitted_who_enrolled = \
                x.number_admitted_who_enrolled * 1000 / x.number_admitted / 10.0
            print x, '% enrolled', x.percent_of_admitted_who_enrolled
            x.save()

        # Other things that we could/should be denormalizing would be done here
