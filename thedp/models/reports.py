from django.db import models
"""
field names are slugified().replace('-', '_') versions of the labels given
in the IPEDS source

"""

__all__ = ['PriceTrend']


class YearBasedInstitutionStatModel(models.Model):
    """ base class """
    year = models.IntegerField(default=1970)
    institution = models.ForeignKey('Institution')

    class Meta:
        abstract = True
        unique_together = ('year', 'institution')


class PriceTrend(YearBasedInstitutionStatModel):
    """ PriceTrend.html """
    on_campus_in_statetotal = models.IntegerField(null=True, blank=True)
    in_state_tuition_and_fees = models.IntegerField(null=True, blank=True)
    out_of_state_tuition_and_fees = models.IntegerField(null=True, blank=True)
