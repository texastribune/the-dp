from django.db import models


class SimpleChartable(models.Model):
    """ Model mixin that enables quick dumps via a template tag """
    chart_series = []

    chart_excluded_fields = ('id',)

    class Meta:
        abstract = True

    def get_chart_field_names(self):
        return [x.name for x in self._meta.fields if x.name not in self.chart_excluded_fields]

    def get_chart_series(self):
        if self.chart_series:
            return self.chart_series
        return [(x, "%s") for x in self.get_chart_field_names()]

    def chart_header(self):
        return [self._meta.get_field(field).verbose_name for field, format in self.get_chart_series()]

    def chart_set(self):
        # TODO pep-0378, needs python 2.7
        return [format % getattr(self, field) for field, format in self.get_chart_series()]
