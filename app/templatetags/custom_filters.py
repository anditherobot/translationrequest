# custom_filters.py
import os
from django import template

register = template.Library()

@register.filter
def endswith(value, suffix):
    return value.endswith(suffix)


@register.filter
def get_filename(value, keep_last_10=False):
    filename = os.path.basename(value)
    if keep_last_10:
        filename = filename[-10:]
    return filename


@register.filter(name='add_class')
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    css_classes += f' {arg}'
    return value.as_widget(attrs={'class': css_classes})

