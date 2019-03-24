from django import template

register = template.Library()


@register.filter
def get_name(value):
    raw_name = value.split('/')[-1]
    cap_name = [i.capitalize() for i in raw_name.split('-')]
    fresh_name = ' '.join(cap_name)
    return fresh_name
