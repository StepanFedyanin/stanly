import requests
from xml.etree import ElementTree as ET

from django.apps import apps

# from mw_calc.models import Chunk as mw_chunk

import logging
logger = logging.getLogger('logfile')


def del_session_keys(request):
    """ удалить значения из сессии
        ---Пока не используется.
    """
    keys_to_del = ('scales', 'order', 'payment', 'ya', 'req', 'json', 'group')
    session = dict(request.session.items())

    for key in session.keys():
        for key_to_del in keys_to_del:
            if key_to_del in key:
                del request.session[key]
                break


def set_calc_session(request, calc_name, key, value):
    """ установить сессию калькулятора session[key] = value """
    if calc_name not in request.session:
        request.session[calc_name] = {}

    session = request.session[calc_name]
    session[key] = value


def get_calc_session(request, calc_name, key, default=None):
    """Вернёт сессию калькулятора """
    if calc_name not in request.session:
        return default

    if key not in request.session[calc_name]:
        return default

    session = request.session[calc_name]
    return session[key]


def isNaN(num):
    """ проверка на NaN"""
    return num != num


def get_app_label_by_calc_name(calc_name):
    """Вернёт название приложения по названию калькулятора """
    if calc_name in ('correlation_spearman', 'correlation_pearson', 'correlation_kendall'):
        app_label = 'correlation'
    else:
        app_label = calc_name

    return app_label


def get_model_name_by_calc_name(calc_name):
    """Вернёт название модели по названию калькулятора """
    if calc_name == 'correlation_spearman':
        model_name = 'ChunkSpearman'
    elif calc_name == 'correlation_pearson':
        model_name = 'ChunkPearson'
    elif calc_name == 'correlation_kendall':
        model_name = 'ChunkKendall'
    else:
        model_name = 'Chunk'

    return model_name


def check_no_pay(request, calc_name):
    """ нужна ли оплата по калькулятору calc_name"""
    no_pay = get_chunk_value_by_name(calc_name, 'no_pay')
    return True if no_pay == '1' else False


def get_chunk_by_calc_name(calc_name):
    """Вернёт  модель калькулятора по его названию """
    model_name = get_model_name_by_calc_name(calc_name)
    app_label = get_app_label_by_calc_name(calc_name)
    return apps.get_model(app_label=app_label, model_name=model_name)


def get_chunk_value_by_name(calc_name, name):
    """
        Вернёт значение параметра калькулятора по названию калькулятора и параметра.
        Если значение не установлено - попытка взять значение у базовой модели mw_calc.
    """
    # Chunk = get_chunk_by_calc_name(calc_name)
    # obj = Chunk.objects.filter(name=name).first()
    # res = None
    #
    # if obj is None or (len(obj.value) == 0 and len(obj.html) == 0):
    #     mw_chunk = apps.get_model(app_label='mw_calc', model_name='Chunk')
    #     obj = mw_chunk.objects.filter(name=name).first()
    #     if obj is None:
    #         return res
    #
    # if len(obj.value) > 0:
    #     res = obj.value
    # else:
    #     res = obj.html

    return name


def getRobokassaPaymentMethods(MerchantLogin, Language='ru'):
    """Получить список способов оплаты"""
    payment_methods_url = 'https://auth.robokassa.ru/Merchant/WebService/Service.asmx/GetCurrencies'
    params = {
        'MerchantLogin': MerchantLogin,
        'Language': Language
    }

    payment_methods = list()

    try:
        res = requests.get(payment_methods_url, params=params)
    except ConnectionError as e:
        logger.debug("getRobokassaPaymentMethods ConnectionError")
        logger.debug(e)
        return False

    prepare = dict()

    if res.status_code == 200:
        # print(res.text)
        try:
            root = ET.fromstring(res.text)
        except:
            res.encoding = "utf-8-sig"
            root = ET.fromstring(res.text)

        for method_group in root.iter('{http://merchant.roboxchange.com/WebService/}Group'):
            group_name = method_group.get('Code')
            prepare[group_name] = list()

            for method in method_group.iter():
                if method.get('Alias'):
                    prepare[group_name].append((
                        method.get('Alias'),
                        method.get('Name'),
                    ))

    for method in prepare:
        payment_methods.append((method, prepare[method]))

    return payment_methods
