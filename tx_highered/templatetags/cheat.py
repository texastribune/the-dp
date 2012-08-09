from django import template

register = template.Library()


@register.filter
def keyvalue(d, key):
    try:
        print key
        return d[key]
    except KeyError:
        return u""
