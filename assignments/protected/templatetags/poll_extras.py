from django import template
import datetime
import html
import re

register = template.Library()

@register.filter(name='from_tuple_to_pretty_date')
def to_pretty_date(value):
    return datetime.datetime(value[0], value[1], value[2]).strftime('%d %B, %Y')


@register.filter(name='highlight_links')
def highlight_links(value):
    regex = re.compile(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|(www\.)?[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})')
    text = html.escape(value)
    sites = {str(m[0]) for m in regex.findall(text)}
    for site in sites:
        text = text.replace(site, '<a class="link" target="_blank" href="{0}">{0}</a>'.format(site))
    return text
