from django import template
import os

register = template.Library()

@register.filter
def format_filename(value):
    filename = os.path.basename(value)
    filename = os.path.splitext(filename)[0]
    formatted_name = filename.replace('_', ' ')
    return formatted_name 