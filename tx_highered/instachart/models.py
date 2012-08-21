from django.db import models


NULL_DISPLAY = "&ndash;"


class ChartCell(object):
    head_attrs = {}
    body_attrs = {}
    label = ""
    format = "%s"
    text = ""
    raw_text = ""

    def __init__(self, cls, fieldname, format=None):
        self.label = fieldname
        try:
            self.field = cls._meta.get_field(fieldname)
            self.text = self.field.verbose_name
        except models.FieldDoesNotExist:
            try:
                self.text = getattr(cls, fieldname).verbose_name
            except AttributeError:
                self.text = fieldname
        self.raw_text = self.text
        if format is not None:
            self.format = format
        if hasattr(cls, 'chart_head_attrs'):
            self.head_attrs = dict(cls.chart_head_attrs)
        if hasattr(cls, 'chart_body_attrs'):
            self.body_attrs = dict(cls.chart_body_attrs)

    def apply_format(self, template):
        try:
            return template % self.raw_text
        except TypeError:
            return template

    def build_attrs(self, attrs, label):
        if label not in attrs:
            return ""
        attr = attrs[label]
        if isinstance(attr, basestring):
            return self.apply_format(attr)
        return u" ".join(map(self.apply_format, attr))

    def as_th(self):
        # TODO get mark_safe to work
        # from django.utils.safestring import mark_safe
        if self.head_attrs and self.label in self.head_attrs:
            return u"<th %s>%s</th>" % (self.build_attrs(self.head_attrs, self.label), self.text)
        return u"<th>%s</th>" % self.text

    def as_td(self):
        if self.body_attrs and self.label in self.body_attrs:
            return u"<td %s>%s</td>" % (self.build_attrs(self.body_attrs, self.label), self.text)
        return u"<td>%s</td>" % self.text

    def as_text(self):
        return self.text

    def __repr__(self):
        return self.as_th()


class ChartBodyCell(ChartCell):
    def __init__(self, obj, fieldname, format=None):
        super(ChartBodyCell, self).__init__(obj, fieldname, format)
        self.raw_text = getattr(obj, fieldname)
        if hasattr(self.raw_text, '__call__'):
            self.raw_text = self.raw_text()
        if self.raw_text is None:
            self.text = NULL_DISPLAY
        else:
            self.text = self.format % self.raw_text

    def as_td_data(self):
        return u"<td data-value=\"%s\">%s</td>" % (self.raw_text, self.text)


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
            # normalize, wrap in tuple if a series was defined simple
            return [(x,) if isinstance(x, basestring) else x for x in cls.chart_series]
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
