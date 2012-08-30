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

    african_american_percent = models.FloatField(null=True,
        verbose_name='% Black')
    asian_percent = models.FloatField(null=True,
        verbose_name='% Asian')
    hispanic_percent = models.FloatField(null=True,
        verbose_name='% Hispanic')
    international_percent = models.FloatField(null=True,
        verbose_name='% International')
    multiracial_percent = models.FloatField(null=True,
        verbose_name='% Multiracial')
    native_american_percent = models.FloatField(null=True,
        verbose_name='% Native Am.')
    pacific_islander_percent = models.FloatField(null=True,
        verbose_name='% Pacific Islander')
    unknown_percent = models.FloatField(null=True,
        verbose_name='% N/A')
    white_percent = models.FloatField(null=True,
        verbose_name='% White')


    def race_data(self):
        race_attrs = [f.attname for f in self._meta.fields
                      if '_percent' in f.attname]
        data = []
        for race_attr in race_attrs:
            value = getattr(self, race_attr, None)
            if value is not None:
                data.append({
                    'year': self.year,
                    'metric': race_attr,
                    'race': self._meta.get_field(race_attr).verbose_name.title(),
                    'enrollment': self.total,
                    'value': value,
                })

        return data
