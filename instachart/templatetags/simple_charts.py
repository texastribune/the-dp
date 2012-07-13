from django import template
from django.template.base import TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


register = template.Library()


# top stuff is directly from armstrong layout_helpers with object renamed obj
@register.tag(name="simple_chart")
def do_render_qs(parser, token):
    tokens = token.split_contents()
    if len(tokens) is 3:
        _, obj, name = tokens
        return RenderQuerysetNode(obj, name)

    message = "Too %s parameters" % ("many" if len(tokens) > 3 else "few")
    raise TemplateSyntaxError(message)


class RenderQuerysetNode(template.Node):
    def __init__(self, qs, name):
        self.qs = template.Variable(qs)
        self.name = template.Variable(name)

    def render(self, context):
        qs = self.qs.resolve(context)
        name = self.name.resolve(context)
        return render_queryset(qs, name, dictionary={}, context_instance=context)


class ChartsRenderQuerysetBackend(object):
    def get_layout_template_name(self, obj, name):
        ret = []
        for a in obj.mro():
            if not hasattr(a, "_meta"):
                continue
            ret.append("layout/%s/%s/%s.html" % (a._meta.app_label,
                a._meta.object_name.lower(), name))
        return ret

    def render(self, qs, name, dictionary=None, context_instance=None):
        dictionary = dictionary or {}
        dictionary["object_list"] = qs
        dictionary["chart_header"] = qs.model.get_chart_header()
        template_name = self.get_layout_template_name(qs.model, name)
        return mark_safe(render_to_string(template_name, dictionary=dictionary,
            context_instance=context_instance))

    def __call__(self, *args, **kwargs):
        return self.render(*args, **kwargs)

render_queryset = ChartsRenderQuerysetBackend()
