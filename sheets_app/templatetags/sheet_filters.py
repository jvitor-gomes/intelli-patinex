from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def format_date(value):
    if not value:
        return ''
    try:
        if isinstance(value, str):
            date_obj = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return date_obj.strftime('%d/%m/%Y')
        elif isinstance(value, datetime):
            return value.strftime('%d/%m/%Y')
        else:
            return value
    except (ValueError, TypeError):
        return value