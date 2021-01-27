from django import template
from random import randint

register = template.Library()


@register.simple_tag
def set_data(value):
    return value
