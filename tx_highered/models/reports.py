from __future__ import division
from collections import namedtuple
import math

from django.db import models

from ..instachart.models import SimpleChart

from .base import APP_LABEL, Institution

"""
field names are slugified().replace('-', '_') versions of the labels given
in the IPEDS source

"""

__all__ = ['PriceTrends', 'TestScores', 'Admissions',
'Enrollment', 'GraduationRates']

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


class InstitutionValueManager(models.Manager):
    def by_year(self, year, **attrs):
        table = self.model._meta.db_table
        institution_table = Institution._meta.db_table

        select = {'year': '%s.year' % table}
        for attr, column in attrs.items():
            select[attr] = '%s.%s' % (table, column)

        return Institution.objects.published().extra(
            tables=[table],
            select=select,
            where=['%s.institution_id = %s.id' % (table, institution_table),
                   '%s.year = %%s' % table],
            params=[year],
        )


class YearBasedInstitutionStatModel(models.Model):
    """ base class """
    YEAR_TYPE_CHOICES = (
        ('academic', 'Academic'),  # 2003-2004
        ('calendar', 'Calendar'),  # 2004
        ('fall', 'Fall'),          # F04
        ('fiscal', 'FY'),          # FY 2010
        ('aug', 'August 31st'))    # August
    year = models.IntegerField(default=1970, verbose_name=u'Year')
    year_type = models.CharField(max_length=10, choices=YEAR_TYPE_CHOICES, null=True)
    institution = models.ForeignKey('Institution', related_name='%(class)s')

    # eehhhh, this doesn't really belong here but whatever
    chart_excluded_fields = ('id', 'institution',)

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
            # return "F%02d" % (int(self.year) % 100)
            return "Fall %s" % self.year
        elif self.year_type == 'fiscal':
            return "FY %s" % self.year
        elif self.year_type == 'aug':
            return "August 31st, %s" % self.year
        return "%d %s" % (self.year, self.year_type)

    @property
    def display_year(self):
        return self.get_display_year()


class PriceTrends(YearBasedInstitutionStatModel, SimpleChart):
    tuition_fees_in_state = models.IntegerField(null=True,
        verbose_name=u"In-State Tuition & Fees")
    tuition_fees_outof_state = models.IntegerField(null=True,
        verbose_name=u"Out-Of-State Tuition & Fees")
    books_and_supplies = models.IntegerField(null=True,
        verbose_name=u"Books & Supplies")
    room_and_board_on_campus = models.IntegerField(null=True)
    room_and_board_off_campus = models.IntegerField(null=True)
    room_and_board_off_campus_w_family = models.IntegerField(null=True)

    data_source = 'IPEDS'

    @property
    def in_state(self):
        return self.tuition_fees_in_state

    @property
    def out_of_state(self):
        return self.tuition_fees_outof_state

    @property
    def in_state_has_risen(self):
        old = self.a_decade_ago
        return old.in_state < self.in_state

    @property
    def out_of_state_has_risen(self):
        old = self.a_decade_ago
        return old.out_of_state < self.out_of_state

    @property
    def a_decade_ago(self):
        if not hasattr(self, '_a_decade_ago'):
            try:
                self._a_decade_ago = (self.institution.pricetrends
                        .filter(year__lte=self.year - 10)
                        .latest('year'))
            except PriceTrends.DoesNotExist:
                self._a_decade_ago = None
        return self._a_decade_ago

    @property
    def in_state_change(self):
        old = self.a_decade_ago
        change = (self.in_state - old.in_state) / old.in_state
        return round(math.ceil(abs(change * 100)))

    @property
    def out_of_state_change(self):
        old = self.a_decade_ago
        change = (self.out_of_state - old.out_of_state) / old.out_of_state
        return round(math.ceil(abs(change * 100)))

    def __unicode__(self):
        return "Price Trends %s %s" % (self.display_year, self.institution)

    chart_series = (('year', "%d"),
                    ('tuition_fees_in_state', "$%d"),
                    ('tuition_fees_outof_state', "$%d"),
                    ('books_and_supplies', "$%d"))

    chart_head_attrs = (('tuition_fees_in_state', ('data-tablebars=1',)),
                        ('tuition_fees_outof_state', 'data-tablebars=1'),
                        ('books_and_supplies', 'data-tablebars=1'))

    chart_body_attrs = (('tuition_fees_in_state', 'data-value="%d"'),
                        ('tuition_fees_outof_state', 'data-value="%d"'),
                        ('books_and_supplies', 'data-value="%d"'))


#############################################################################
#   Admissions
#############################################################################

class TestScoresManager(models.Manager):
    def latest(self):
        return super(TestScoresManager, self).latest('year')

    def oldest(self):
        return self.order_by('year')[0]


class TestScores(YearBasedInstitutionStatModel):
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

    data_source = 'IPEDS'

    objects = TestScoresManager()

    def __unicode__(self):
        return "Test Scores %s %s" % (self.display_year, self.institution)

    def __json__(self):
        return {
            'year': self.year,
            'sat': {
                'verbal': [self.sat_verbal_25th_percentile, self.sat_verbal_75th_percentile],
                'math': [self.sat_math_25th_percentile, self.sat_math_75th_percentile],
                'writing': [self.sat_writing_25th_percentile, self.sat_writing_75th_percentile],
                'submitted_number': self.sat_submitted_number,
                'submitted_percent': self.sat_submitted_percent,
            },
            'act': {
                'verbal': [self.act_english_25th_percentile, self.act_english_75th_percentile],
                'math': [self.act_math_25th_percentile, self.act_math_75th_percentile],
                'writing': [self.act_writing_25th_percentile, self.act_writing_75th_percentile],
                'composite': [self.act_composite_25th_percentile, self.act_composite_75th_percentile],
                'submitted_number': self.act_submitted_number,
                'submitted_percent': self.act_submitted_percent,
            },
        }

    @property
    def sat_verbal_range(self):
        return "%s - %s" % (self.sat_verbal_25th_percentile,
                self.sat_verbal_75th_percentile)

    @property
    def sat_verbal_range_english(self):
        return self.sat_verbal_range.replace(' - ', ' to ')

    @property
    def sat_math_range(self):
        return "%s - %s" % (self.sat_math_25th_percentile,
                self.sat_math_75th_percentile)

    @property
    def sat_math_range_english(self):
        return self.sat_math_range.replace(' - ', ' to ')

    @property
    def sat_writing_range(self):
        if self.sat_writing_25th_percentile:
            return "%s - %s" % (self.sat_writing_25th_percentile,
                    self.sat_writing_75th_percentile)
        else:
            return ""

    @property
    def sat_writing_range_english(self):
        return self.sat_writing_range.replace(' - ', ' to ')

    @property
    def bar(self):
        if hasattr(self, '_bar'):
            return self._bar
        HorizontalBar = namedtuple('HorizontalBar', ['left', 'width'])
        context = dict()
        min, max = 300, 800 * 1.05  # yeah yeah, i'm overriding max and min
        w = (max - min) / 100
        if self.sat_verbal_25th_percentile:
            context['sat_v'] = HorizontalBar((self.sat_verbal_25th_percentile - min) / w,
                      (self.sat_verbal_75th_percentile - self.sat_verbal_25th_percentile) / w)
        if self.sat_math_25th_percentile:
            context['sat_m'] = HorizontalBar((self.sat_math_25th_percentile - min) / w,
                      (self.sat_math_75th_percentile - self.sat_math_25th_percentile) / w)
        if self.sat_writing_25th_percentile:
            context['sat_w'] = HorizontalBar((self.sat_writing_25th_percentile - min) / w,
                      (self.sat_writing_75th_percentile - self.sat_writing_25th_percentile) / w)

        min, max = 10, 36 * 1.05
        w = (max - min) / 100
        if self.act_english_25th_percentile:
            context['act_e'] = HorizontalBar((self.act_english_25th_percentile - min) / w,
                      (self.act_english_75th_percentile - self.act_english_25th_percentile) / w)
        if self.act_math_25th_percentile:
            context['act_m'] = HorizontalBar((self.act_math_25th_percentile - min) / w,
                      (self.act_math_75th_percentile - self.act_math_25th_percentile) / w)
        if self.act_composite_25th_percentile:
            context['act_c'] = HorizontalBar((self.act_composite_25th_percentile - min) / w,
                      (self.act_composite_75th_percentile - self.act_composite_25th_percentile) / w)
        min, max = 2, 12 * 1.05
        w = (max - min) / 100
        if self.act_writing_25th_percentile:
            context['act_w'] = HorizontalBar((self.act_writing_25th_percentile - min) / w,
                      (self.act_writing_75th_percentile - self.act_writing_25th_percentile) / w)
        self._bar = context
        return context

    @property
    def sat_verbal_width(self):
        return self.sat_verbal_75th_percentile - self.sat_verbal_25th_percentile


class AdmissionsManager(models.Manager):
    def latest(self):
        return super(AdmissionsManager, self).latest('year')

    def oldest(self):
        return self.order_by('year')[0]


class Admissions(YearBasedInstitutionStatModel, SimpleChart):
    number_of_applicants = models.IntegerField(null=True, blank=True)
    number_admitted = models.IntegerField(null=True, blank=True)
    number_admitted_who_enrolled = models.IntegerField(null=True, blank=True)
    percent_of_applicants_admitted = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name=u"%admitted")
    percent_of_admitted_who_enrolled = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name=u"%admitted who enrolled")
    percent_top10rule = models.DecimalField(max_digits=4, decimal_places=1,
        null=True, verbose_name="First-Time Students in Top 10%")

    data_source = 'IPEDS'

    objects = AdmissionsManager()

    def __unicode__(self):
        return "Admissions Data %s %s" % (self.display_year, self.institution)

    class Meta(YearBasedInstitutionStatModel.Meta):
        get_latest_by = 'year'


class Enrollment(YearBasedInstitutionStatModel, SimpleChart):
    institution_values = InstitutionValueManager()
    objects = models.Manager()

    total = models.IntegerField(null=True)
    fulltime_equivalent = models.IntegerField(null=True,
        verbose_name='Full-time Equivalent')
    fulltime = models.IntegerField(null=True, verbose_name='Full-time')
    parttime = models.IntegerField(null=True, verbose_name='Part-time')
    # TODO better list that works with IPEDS and THECB
    total_percent_white = models.IntegerField(null=True,
        verbose_name='% White')
    total_percent_black = models.IntegerField(null=True,
        verbose_name='% Black')
    total_percent_hispanic = models.IntegerField(null=True,
        verbose_name='% Hispanic')
    total_percent_native = models.IntegerField(null=True,
        verbose_name='% Native Am.')
    total_percent_asian = models.IntegerField(null=True,
        verbose_name='% Asian')
    total_percent_unknown = models.IntegerField(null=True,
        verbose_name='% N/A')

    data_source = 'IPEDS'

    def __unicode__(self):
        return "Enrollment Data %s %s" % (self.display_year, self.institution)

    race_attrs = ['total_percent_%s' % race for race in
            ('white', 'black', 'hispanic', 'native', 'asian', 'unknown')]

    def race_data(self):
        data = []
        for race_attr in self.race_attrs:
            value = getattr(self, race_attr, None)
            if value is not None:
                data.append({
                    'year': self.year,
                    'metric': race_attr,
                    'race': self._meta.get_field(race_attr).verbose_name,
                    'enrollment': self.total,
                    'value': value,
                })

        return data

    chart_series = ('year',
                    'fulltime_equivalent',
                    'fulltime',
                    'parttime',) + tuple(race_attrs)


class GraduationRates(YearBasedInstitutionStatModel, SimpleChart):
    bachelor_4yr = models.IntegerField(null=True,
        verbose_name=u"Bachelor degree within four years")
    bachelor_5yr = models.IntegerField(null=True,
        verbose_name=u"Bachelor degree within five years")
    bachelor_6yr = models.IntegerField(null=True,
        verbose_name=u"Bachelor degree within six years")

    data_source = 'IPEDS'

    def __unicode__(self):
        return "Graduation Rates %s %s" % (self.display_year, self.institution)

    chart_series = ('display_year',
                    ('bachelor_4yr', "%s%%"),
                    ('bachelor_5yr', "%s%%"),
                    ('bachelor_6yr', "%s%%"))
