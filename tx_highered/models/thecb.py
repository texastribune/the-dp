from __future__ import division

from django.db import models

from .reports import YearBasedInstitutionStatModel


__all__ = ['PublicEnrollment']


"""
RACES = [
    ,
    'American Indian/Alaskan Native',
    'Asian',
    'Hispanic',
    'International',
    'Multiracial',
    'Native Hawaiian/Pacific Island',
    'Unknown or Not Reported',
    'White',
]
"""


class PublicEnrollment(YearBasedInstitutionStatModel):
    total = models.IntegerField(null=True)

    african_american_count = models.IntegerField(null=True)
    asian_count = models.IntegerField(null=True)
    hispanic_count = models.IntegerField(null=True)
    international_count = models.IntegerField(null=True)
    multiracial_count = models.IntegerField(null=True)
    native_american_count = models.IntegerField(null=True)
    pacific_islander_count = models.IntegerField(null=True)
    unknown_count = models.IntegerField(null=True)
    white_count = models.IntegerField(null=True)

    african_american_percent = models.FloatField(null=True)
    asian_percent = models.FloatField(null=True)
    hispanic_percent = models.FloatField(null=True)
    international_percent = models.FloatField(null=True)
    multiracial_percent = models.FloatField(null=True)
    native_american_percent = models.FloatField(null=True)
    pacific_islander_percent = models.FloatField(null=True)
    unknown_percent = models.FloatField(null=True)
    white_percent = models.FloatField(null=True)
