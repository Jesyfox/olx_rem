from django import template

register = template.Library()


@register.filter
def get_name(value):
    raw_name = value.split('/')[-1]
    fresh_name = ' '.join(raw_name.split('-'))
    return fresh_name
