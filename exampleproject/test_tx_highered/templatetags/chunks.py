from django import template

register = template.Library()


@register.simple_tag
def chunk(key):
    """Dummy `chunks` tag implementation so templates don't error"""
    return '<!-- chunk {} -->'.format(key)
