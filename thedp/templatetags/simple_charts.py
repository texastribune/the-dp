from django import template
from django.template.base import TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


register = template.Library()


# top stuff is directly from armstrong layout_helpers with object renamed obj
@register.tag(name="simple_chart")
def do_render_model(parser, token):
    tokens = token.split_contents()
    if len(tokens) is 3:
        _, obj, name = tokens
        return RenderObjectNode(obj, name)

    message = "Too %s parameters" % ("many" if len(tokens) > 3 else "few")
    raise TemplateSyntaxError(message)


class RenderObjectNode(template.Node):
    def __init__(self, obj, name):
        self.obj = template.Variable(obj)
        self.name = template.Variable(name)

    def render(self, context):
        obj = self.obj.resolve(context)
        name = self.name.resolve(context)
        return render_model(obj, name, dictionary={}, context_instance=context)


class ChartsRenderModelBackend(object):
    def get_layout_template_name(self, model, name):
        ret = []
        for a in model.mro():
            if not hasattr(a, "_meta"):
                continue
            ret.append("layout/%s/%s/%s.html" % (a._meta.app_label,
                a._meta.object_name.lower(), name))
        return ret

    def render(self, obj, name, dictionary=None, context_instance=None):
        dictionary = dictionary or {}
        object_list = getattr(obj, name)
        dictionary["object_list"] = object_list.all()
        template_name = self.get_layout_template_name(object_list.model, "simple_chart")
        return mark_safe(render_to_string(template_name, dictionary=dictionary,
            context_instance=context_instance))

    def __call__(self, *args, **kwargs):
        return self.render(*args, **kwargs)

render_model = ChartsRenderModelBackend()
