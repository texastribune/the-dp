from django import template
from django.template import loader
from django.template.base import TemplateSyntaxError
from django.utils.safestring import mark_safe

from ..models import SimpleChart, ChartCell


DEFAULT_CHART_NAME = "simple_chart"

register = template.Library()


# top stuff is directly from armstrong layout_helpers with object renamed obj
@register.tag(name="instachart")
def do_render_qs(parser, token):
    tokens = token.split_contents()
    if len(tokens) is 2:
        tokens.append(u'"%s"' % DEFAULT_CHART_NAME)
    if len(tokens) is 3:
        _, obj, name = tokens
        return RenderQuerysetNode(obj, name)

    message = "Too %s parameters" % ("many" if len(tokens) > 3 else "few")
    raise TemplateSyntaxError(message)


class RenderQuerysetNode(template.Node):
    def __init__(self, qs, name):
        self.qs = template.Variable(qs)
        self.name = template.Variable(name)

    def get_layout_template_name(self, obj, name):
        ret = []
        for a in obj.mro():
            if not hasattr(a, "_meta"):
                continue
            ret.append("instachart/%s/%s.html" % (a._meta.object_name.lower(), name))
        return ret

    def render(self, context):
        qs = self.qs.resolve(context)
        name = self.name.resolve(context)

        dictionary = {}
        dictionary["object_list"] = qs
        try:
            dictionary["chart_header"] = qs.model.get_chart_header()
            template_name = self.get_layout_template_name(qs.model, name)
        except AttributeError:
            fields = [x.name for x in qs.model._meta.fields]
            dictionary["chart_header"] = [ChartCell(qs.model, field) for field in fields]
            template_name = ["instachart/simplechart/%s.html" % name]

        template = loader.select_template(template_name)

        with context.push(dictionary):
            string = template.template.render(context)
        return mark_safe(string)


@register.filter(name="chart_set")
def chart_set(obj):
    return SimpleChart.chart_set(obj)
