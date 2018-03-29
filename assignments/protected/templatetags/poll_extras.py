from django import template
import datetime

register = template.Library()

@register.filter(name='from_tuple_to_pretty_date')
def to_pretty_date(value):
    return datetime.datetime(value[0], value[1], value[2]).strftime('%d %B, %Y')
