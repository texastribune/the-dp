from django.db import models


NULL_DISPLAY = "&ndash;"


class ChartCell(object):
    attrs = []
    format = "%s"
    text = ""

    def __init__(self, cls, fieldname, format=None, attrs=None):
        try:
            self.field = cls._meta.get_field(fieldname)
            self.text = self.field.verbose_name
        except models.FieldDoesNotExist:
            self.text = fieldname
        if format is not None:
            self.format = format
        if attrs is not None:
            self.attrs = attrs

    def as_th(self):
        # TODO get mark_safe to work
        # from django.utils.safestring import mark_safe
        return u"<th %s>%s</th>" % (u" ".join(self.attrs), self.text)

    def as_td(self):
        return u"<td>%s</td>" % self.text

    def as_text(self):
        return self.text

    def __repr__(self):
        return self.as_th()


class ChartBodyCell(ChartCell):
    def __init__(self, obj, fieldname, format=None, attrs=None):
        if format is not None:
            self.format = format
        if attrs is not None:
            self.attrs = attrs
        self.value = getattr(obj, fieldname)
        if self.value is None:
            self.text = NULL_DISPLAY
        else:
            self.text = self.format % self.value

    def as_td_data(self):
        return u"<td data-value=\"%s\">%s</td>" % (self.value, self.text)


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
        return [ChartCell(cls, *x) for x in cls.get_chart_series()]

    @staticmethod
    def chart_set(obj):
        # TODO pep-0378, needs python 2.7
        try:
            cells = [ChartBodyCell(obj, *x) for x in obj.get_chart_series()]
        except AttributeError:
            fields = [x.name for x in obj._meta.fields]
            cells = [ChartBodyCell(obj, field) for field in fields]
        return cells
