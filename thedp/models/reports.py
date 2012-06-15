from django.db import models
"""
field names are slugified().replace('-', '_') versions of the labels given
in the IPEDS source

"""

__all__ = ['PriceTrend', 'SATTestScores']


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
