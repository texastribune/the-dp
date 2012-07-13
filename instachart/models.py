from django.db import models


class th(object):
    attrs = []
    format = "%s"

    def __init__(self, field, format, attrs=None):
        self.field = field
        if format:
            self.format = format
        self.attrs = attrs

    def __repr__(self):
        return self.field.verbose_name


class SimpleChart(models.Model):
    """ Model mixin that enables quick dumps via a template tag """
    chart_series = []

    chart_excluded_fields = ('id',)

    class Meta:
        abstract = True

    @classmethod
    def get_chart_field_names(cls):
        return [x.name for x in cls._meta.fields if x.name not in cls.chart_excluded_fields]

    @classmethod
    def get_chart_series(cls):
        if cls.chart_series:
            return cls.chart_series
        return [(x, "%s") for x in cls.get_chart_field_names()]

    @classmethod
    def get_chart_header(cls):
        return [th(cls._meta.get_field(x[0]), *x[1:]) for x in cls.get_chart_series()]

    @staticmethod
    def chart_set(obj):
        # TODO pep-0378, needs python 2.7
        try:
            cells = [format % getattr(obj, field) for field, format in obj.get_chart_series()]
        except AttributeError:
            fields = [x.name for x in obj._meta.fields]
            cells = [getattr(obj, field) for field in fields]
        return cells
