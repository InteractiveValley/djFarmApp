# -*- encoding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
register = template.Library()


@register.filter(name='currency')
def currency(value):
    value = round(float(value), 2)
    return "$%s%s" % (intcomma(int(value)), ("%0.2f" % value)[-3:])


@register.filter(name='quantity')
def quantity(value):
    value = round(float(value), 2)
    return "%s%s" % (intcomma(int(value)), ("%0.0f" % value)[-3:])


@register.filter(name='avg_send')
def avg_send(value):
    return "%s" % (str(value) + "%",)