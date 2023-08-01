# custom_filters.py
from django import template

register = template.Library()

@register.filter
def endswith(value, suffix):
    return value.endswith(suffix)

