# app/templatetags/custom_filters.py
from django import template
from .custom_filters import endswith  # Import the custom filter from custom_filters.py

register = template.Library()

# Register the custom filter
register.filter('endswith', endswith)

