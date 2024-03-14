from django import template
from django.conf import settings as s

from mw_calc.helpers import get_chunk_value_by_name
from mw_calc.utils import is_paid

register = template.Library()


def get_session_var(request, var):
    if var in request.session:
        return request.session[var]
    return False


@register.simple_tag(takes_context=True)
def get_session_order_id(context):
    request = context['request']
    return get_session_var(request, 'order_id')


@register.simple_tag
def get_chunk(name, calc_name='mw_calc'):
    return get_chunk_value_by_name(calc_name, name) or ''


@register.simple_tag
def get_static_version():
    return "?v=0311202100"


# @register.simple_tag(takes_context=True)
# def get_host_name(context):
#     request = context['request']
#     return request.host


@register.simple_tag(takes_context=True)
def get_profile_pay_status(context):
    request = context['request']

    for calc_name in s.CALC_NAMES:
        if is_paid(request, calc_name):
                return True
    
    return False


@register.simple_tag(takes_context=True)
def get_session_step(context):
    request = context['request']
    return get_session_var(request, 'session_step')


@register.simple_tag
def get_VK_APP_ID():
    return s.VK_APP_ID


@register.simple_tag
def get_G_RECAPTCHA_KEY():
    return s.G_RECAPTCHA_KEY


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)
