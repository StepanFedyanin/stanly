import os

import logging
from django.utils import timezone
# from django.apps import apps
from django.http import HttpResponseRedirect
from django.conf import settings as s

from .models import Order, Calculation
# from .forms import robokassa_form
from .helpers import check_no_pay, get_chunk_value_by_name
from .utils import is_paid

logger = logging.getLogger('logfile')


def check_payment(get):
    """ декоратор.  Проверка, оплачен ли текущий калькулятор из request"""

    def wrapper(self, request, *args, **kwargs):
        calc_name = self.calc_name

        if 'correlation_name' in self.kwargs:
            calc_name = self.kwargs['correlation_name']

        paid_order = is_paid(request, calc_name)

        # logger.debug(paid_order)
        # print(paid_order)

        if request.user.is_superuser or paid_order or check_no_pay(request, calc_name):
        # if paid_order or check_no_pay(request, calc_name):
            return get(self, request, *args, **kwargs)
        else:
            return HttpResponseRedirect(f'{s.CALC_INDEX_URL}accounts/profile/')

    return wrapper


def get_calcs(profile):
    """ декоратор.  возвращает функцию-контекст по всем калькуляторам """
    def wrapper(request):

        calcs = ([_get_calc_context(request, calc_name) for calc_name in s.CALC_NAMES])

        return profile(request, calcs=calcs)

    return wrapper


def _get_calc_context(request, calc_name):
    """ получить контекст калькулятора
    
    Args:
        request: объект запроса
        calc_name: калькулятор, строка
    
    Returns:
        калькулятор: 
            форма оплаты
            оплаченные расчёты
            вычисления
            нужно ли платить за кулькулятор
    """
    price_type = request.session['price_type']
    price = get_chunk_value_by_name(calc_name, price_type) or \
            get_chunk_value_by_name(calc_name, 'price')

    price = int(price) if price is str else 0
    user = request.user

    calculation = Calculation.objects.filter(
        user=user,
        calc_name=calc_name
    )
    calculation_total = len(calculation)

    pay = {
        'price': price,
        'calc_name': calc_name
    }

    result = {calc_name: {
        "paid_order": is_paid(request, calc_name),
        "calculation": calculation,
        "calculation_total": calculation_total,
        "no_pay": check_no_pay(request, calc_name),
        "translate": s.CALC_NAMES_TRANS[calc_name],
        'url': os.path.join(request.path, calc_name),
        'pay': pay
    }}

    # print(result)

    # if not paid_orders:
    #     Order.objects.get_or_create(
    #         user=user,
    #         calc_name=calc_name,
    #         status='',
    #         price=price
    #     )

    #     result[calc_name]['form'] = robokassa_form(request, calc_name)

    return result
