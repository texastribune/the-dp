from __future__ import division

from django.db import models

from .reports import (YearBasedInstitutionStatModel, AdmissionsManager,
        InstitutionValueManager)
from ..instachart.models import SimpleChart


__all__ = ['PublicEnrollment', 'PublicGraduationRates', 'PublicAdmissions']


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


class PublicEnrollment(YearBasedInstitutionStatModel, SimpleChart):
    institution_values = InstitutionValueManager()
    objects = models.Manager()

    total = models.IntegerField(null=True, help_text='Total full-time students')
    # TODO fulltime_equivalent = models.IntegerField(null=True,
    #    verbose_name='Full-time Equivalent')

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
        verbose_name='% Unknown')
    white_percent = models.FloatField(null=True,
        verbose_name='% White')

    data_source = 'THECB'

    @property
    def total_percent_white(self):
        return self.white_percent

    @property
    def total_percent_black(self):
        return self.african_american_percent

    @property
    def total_percent_hispanic(self):
        return self.hispanic_percent

    @property
    def total_percent_native(self):
        return self.native_american_percent

    @property
    def total_percent_asian(self):
        return self.asian_percent

    @property
    def total_percent_unknown(self):
        return self.unknown_percent

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

    race_attrs = ['total_percent_%s' % race for race in
            ('white', 'black', 'hispanic', 'native', 'asian', 'unknown')]

    chart_series = (('year', 'total') +
                    tuple(race_attrs) +
                    ('international_percent', 'multiracial_percent',
                     'pacific_islander_percent'))


class PublicGraduationRates(YearBasedInstitutionStatModel, SimpleChart):
    associate_3yr = models.DecimalField(null=True,
        max_digits=5, decimal_places=2,
        verbose_name=u"Associate degree within three years",
        help_text=u"Only available for community colleges")
    associate_4yr = models.DecimalField(null=True,
        max_digits=5, decimal_places=2,
        verbose_name=u"Associate degree within four years",
        help_text=u"Only available for community colleges")
    associate_6yr = models.DecimalField(null=True,
        max_digits=5, decimal_places=2,
        verbose_name=u"Associate degree within six years",
        help_text=u"Only available for community colleges")

    bachelor_3yr = models.DecimalField(null=True,
        max_digits=5, decimal_places=2,
        verbose_name=u"Bachelor degree within three years",
        help_text=u"Only available for community colleges")
    bachelor_4yr = models.DecimalField(null=True,
        max_digits=5, decimal_places=2,
        verbose_name=u"Bachelor degree within four years")
    bachelor_5yr = models.DecimalField(null=True,
        max_digits=5, decimal_places=2,
        verbose_name=u"Bachelor degree within five years")
    bachelor_6yr = models.DecimalField(null=True,
        max_digits=5, decimal_places=2,
        verbose_name=u"Bachelor degree within six years")

    data_source = 'THECB'

    def __unicode__(self):
        return "Graduation Rates %s %s" % (self.display_year, self.institution)

    chart_series = ('display_year',
                    ('bachelor_4yr', "%s%%"),
                    ('bachelor_5yr', "%s%%"),
                    ('bachelor_6yr', "%s%%"))


class PublicAdmissions(YearBasedInstitutionStatModel, SimpleChart):
    number_of_applicants = models.IntegerField(null=True, blank=True)
    number_admitted = models.IntegerField(null=True, blank=True)
    number_admitted_who_enrolled = models.IntegerField(null=True, blank=True)
    percent_of_applicants_admitted = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name=u"%admitted")
    percent_of_admitted_who_enrolled = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name=u"%admitted who enrolled")

    data_source = 'THECB'

    objects = AdmissionsManager()

    class Meta(YearBasedInstitutionStatModel.Meta):
        get_latest_by = 'year'
