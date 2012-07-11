from django.db import models

from .base import APP_LABEL

"""
field names are slugified().replace('-', '_') versions of the labels given
in the IPEDS source

"""

__all__ = ['PriceTrend', 'TestScores', 'Admissions', 'Degreescertificates',
'Enrollmentbystudentlevel']

# GENDER_CHOICES = (
#     ('Men', 'Men'),
#     ('Women', 'Women'),
#     ('Total', 'Total'))


# RACE_CHOICES = (
#     ('nra', 'Nonresident alien'),
#     ('white', 'White'),
#     ('black', 'African American'),
#     ('hispanic', 'Hispanic'),
#     ('native', 'Native American'),
#     ('asian', 'Asian/Pacific'),
#     ('unknown', 'Race/ethnicity unknown'))


# IPEDS_RACE_CHOICES = (
#     ('nra', 'Nonresident alien'),
#     ('white', 'White non-Hispanic'),
#     ('black', 'Black non-Hispanic'),
#     ('hispanic', 'Hispanic'),
#     ('native', 'American Indian or Alaska Native'),
#     ('asian', 'Asian or Pacific Islander'),
#     ('unknown', 'Race/ethnicity unknown'))


class YearBasedInstitutionStatModel(models.Model):
    """ base class """
    YEAR_TYPE_CHOICES = (
        ('academic', 'Academic'),  # 2003-2004
        ('calendar', 'Calendar'),  # 2004
        ('fall', 'Fall'))          # F04
    year = models.IntegerField(default=1970, verbose_name=u'Year')
    year_type = models.CharField(max_length=10, choices=YEAR_TYPE_CHOICES, null=True)
    institution = models.ForeignKey('Institution')

    class Meta:
        abstract = True
        app_label = APP_LABEL
        ordering = ['year']
        unique_together = ('year', 'institution')

    def __unicode__(self):
        return u"%s" % self.year

    def get_display_year(self):
        if not self.year_type or self.year_type == 'calendar':
            return self.year
        elif self.year_type == 'academic':
            return "%d-%d" % (self.year - 1, self.year)
        elif self.year_type == 'fall':
            return "F%02d" % (self.year % 100)
        return "%d %s" % (self.year, self.year_type)

    @property
    def display_year(self):
        return self.get_display_year()


# XXX
class SimpleChartable(models.Model):
    chart_series = []

    class Meta:
        abstract = True
        app_label = 'chart'

    def get_chart_series(self):
        if self.chart_series:
            return self.chart_series
        return [(x, "%s") for x in self._meta.get_all_field_names()]

    def chart_header(self):
        return [self._meta.get_field(field).verbose_name for field, format in self.get_chart_series()]

    def chart_set(self):
        # TODO pep-0378, needs python 2.7
        return [format % getattr(self, field) for field, format in self.get_chart_series()]


# class GenderFieldsMixin(models.Model):
#     gender = models.TextField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)

#     class Meta:
#         abstract = True


# def make_int_fields(name, fields, prefix=''):
#     """ Created a model mixin with a series of IntegerFields """
#     attrs = dict()

#     for field in fields:
#         attrs['%s%s' % (prefix, field)] = models.IntegerField(null=True, blank=True)

#     attrs['Meta'] = type('Meta', (), dict(
#                         abstract=True,
#                     ))
#     # attrs['__module__'] = 'schools'

#     return type(name, (models.Model,), attrs)


# EthnicFieldsMixin = make_int_fields('EthnicFieldsMixin', dict(RACE_CHOICES).keys(), prefix='total_')


class PriceTrend(YearBasedInstitutionStatModel, SimpleChartable):
    """ PriceTrend.html """
    on_campus_in_statetotal = models.IntegerField(null=True, blank=True)
    in_state_tuition_and_fees = models.IntegerField(null=True, blank=True)
    out_of_state_tuition_and_fees = models.IntegerField(null=True, blank=True)

    chart_series = (('year', "%d"),
                    ('on_campus_in_statetotal', "$%d"),
                    ('in_state_tuition_and_fees', "$%d"),
                    ('out_of_state_tuition_and_fees', "$%d"))


#############################################################################
#   Admissions
#############################################################################
class TestScores(YearBasedInstitutionStatModel, SimpleChartable):
    # possible data sources: IPEDS
    sat_verbal_25th_percentile = models.IntegerField(null=True)
    sat_verbal_75th_percentile = models.IntegerField(null=True)
    sat_math_25th_percentile = models.IntegerField(null=True)
    sat_math_75th_percentile = models.IntegerField(null=True)
    sat_writing_25th_percentile = models.IntegerField(null=True)
    sat_writing_75th_percentile = models.IntegerField(null=True)
    sat_submitted_number = models.IntegerField(null=True)
    sat_submitted_percent = models.IntegerField(null=True)
    act_composite_25th_percentile = models.IntegerField(null=True)
    act_composite_75th_percentile = models.IntegerField(null=True)
    act_english_25th_percentile = models.IntegerField(null=True)
    act_english_75th_percentile = models.IntegerField(null=True)
    act_math_25th_percentile = models.IntegerField(null=True)
    act_math_75th_percentile = models.IntegerField(null=True)
    act_writing_25th_percentile = models.IntegerField(null=True)
    act_writing_75th_percentile = models.IntegerField(null=True)
    act_submitted_number = models.IntegerField(null=True)
    act_submitted_percent = models.IntegerField(null=True)


# class GenderManager(models.Manager):
#     def men(self):
#         return self.get_query_set().filter(gender='Men')

#     def women(self):
#         return self.get_query_set().filter(gender='Women')

#     def total(self):
#         return self.get_query_set().filter(gender='Total')


class Admissions(YearBasedInstitutionStatModel):
    # TODO make a gender/year based? what about ethnicity?
    number_of_applicants = models.IntegerField(null=True, blank=True)
    number_admitted = models.IntegerField(null=True, blank=True)
    number_admitted_who_enrolled = models.IntegerField(null=True, blank=True)
    percent_of_applicants_admitted = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    percent_of_admitted_who_enrolled = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    # objects = GenderManager()

    class Meta(YearBasedInstitutionStatModel.Meta):
        unique_together = ('year', 'institution')


# TODO better name
class Enrollmentbystudentlevel(YearBasedInstitutionStatModel, SimpleChartable):
    # these choices are how they are found in the CSV
    LEVEL_CHOICES = (
        ('undergrad', 'Undergraduate total'),
        ('grad', 'Graduate'),
        ('pro', 'First-professional'),
        ('gradpro', 'Graduate and first-professional'),
        ('total', 'All students total'))
    student_level = models.CharField(max_length=40, choices=LEVEL_CHOICES, null=True, blank=True)
    full_time_men = models.IntegerField(null=True, blank=True)
    full_time_women = models.IntegerField(null=True, blank=True)
    full_time_total = models.IntegerField(null=True, blank=True)
    part_time_men = models.IntegerField(null=True, blank=True)
    part_time_women = models.IntegerField(null=True, blank=True)
    part_time_total = models.IntegerField(null=True, blank=True)
    grand_total = models.IntegerField(null=True, blank=True)

    class Meta(YearBasedInstitutionStatModel.Meta):
        unique_together = ('year', 'institution', 'student_level')


class Degreescertificates(YearBasedInstitutionStatModel):
    value = models.IntegerField(null=True, blank=True)

    class Meta(YearBasedInstitutionStatModel.Meta):
        unique_together = ('year', 'institution')
