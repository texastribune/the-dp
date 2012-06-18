from django.db import models
"""
field names are slugified().replace('-', '_') versions of the labels given
in the IPEDS source

"""

__all__ = ['PriceTrend', 'SATTestScores', 'Admissions']

GENDER_CHOICES = (
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Total', 'Total'))


class YearBasedInstitutionStatModel(models.Model):
    """ base class """
    year = models.IntegerField(default=1970)
    institution = models.ForeignKey('Institution')

    class Meta:
        abstract = True
        app_label = 'thedp'
        ordering = ['year']
        unique_together = ('year', 'institution')

    def __unicode__(self):
        return u"%d" % self.year


class PriceTrend(YearBasedInstitutionStatModel):
    """ PriceTrend.html """
    on_campus_in_statetotal = models.IntegerField(null=True, blank=True)
    in_state_tuition_and_fees = models.IntegerField(null=True, blank=True)
    out_of_state_tuition_and_fees = models.IntegerField(null=True, blank=True)


class SATTestScores(YearBasedInstitutionStatModel):
    sat_i_verbal_25th_percentile = models.IntegerField(null=True, blank=True)
    sat_i_verbal_75th_percentile = models.IntegerField(null=True, blank=True)
    sat_i_math_25th_percentile = models.IntegerField(null=True, blank=True)
    sat_i_math_75th_percentile = models.IntegerField(null=True, blank=True)
    students_submitting_sat_scores_number = models.IntegerField(null=True, blank=True)
    students_submitting_sat_scores_percent = models.IntegerField(null=True, blank=True)


class GenderManager(models.Manager):
    def men(self):
        return self.get_query_set().filter(gender='Men')

    def women(self):
        return self.get_query_set().filter(gender='Women')

    def total(self):
        return self.get_query_set().filter(gender='Total')


class Admissions(YearBasedInstitutionStatModel):
    # TODO make a gender/year based? what about ethnicity?
    gender = models.TextField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    number_of_applicants = models.IntegerField(null=True, blank=True)
    number_admitted = models.IntegerField(null=True, blank=True)
    number_admitted_who_enrolled = models.IntegerField(null=True, blank=True)
    percent_of_applicants_admitted = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    percent_of_admitted_who_enrolled = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    objects = GenderManager()

    class Meta(YearBasedInstitutionStatModel.Meta):
        unique_together = ('year', 'institution', 'gender')
