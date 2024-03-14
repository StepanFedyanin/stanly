import random
import logging
import requests
import time

from requests.exceptions import ConnectionError
from django import forms
# from django.apps import apps
from django.conf import settings as s
from django.db.models import Q

from xml.etree import ElementTree as ET
from allauth.account.forms import LoginForm, SignupForm, AddEmailForm, ResetPasswordForm, ResetPasswordKeyForm
from robokassa.forms import RobokassaForm
from lk.models import Promo

from .models import Order
from .helpers import get_chunk_value_by_name, getRobokassaPaymentMethods

logger = logging.getLogger('logfile')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class StepLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = False
        self.fields['password'].label = False
        self.fields['login'].widget.attrs.update({'class': 'input'})
        self.fields['password'].widget.attrs.update({'class': 'input'})
        self.fields['login'].widget.attrs.update({'autofocus': False})


class AjaxLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = False
        self.fields['password'].label = False
        self.fields['login'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['password'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['remember'].widget.attrs.update({'class': 'popup-form__checkbox checkbox'})


class StepSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = False
        self.fields['email'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False
        self.fields['username'].widget.attrs.update({'class': 'input'})
        self.fields['email'].widget.attrs.update({'class': 'input'})
        self.fields['password1'].widget.attrs.update({'class': 'input'})
        self.fields['password2'].widget.attrs.update({'class': 'input'})
        self.fields['username'].widget.attrs.update({'autofocus': False})


class AjaxSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = False
        self.fields['email'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False
        self.fields['username'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['email'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['password1'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['password2'].widget.attrs.update({'class': 'popup-form__input input'})


class ProfileLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['password'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['remember'].widget.attrs.update({'class': 'popup-form__checkbox checkbox'})


class ProfileSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['email'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['password1'].widget.attrs.update({'class': 'popup-form__input input'})
        self.fields['password2'].widget.attrs.update({'class': 'popup-form__input input'})


class ProfileAddEmailForm(AddEmailForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = False
        self.fields['email'].widget.attrs.update({'class': ' profile-page__add-email-input input'})


class AjaxResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'popup-form__input input'})


class ProfileResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = False
        self.fields['email'].widget.attrs.update({'class': 'popup-form__input input'})


class ProfileResetPasswordKeyForm(ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = False
        self.fields['password2'].label = False
        self.fields['password1'].widget.attrs.update(
            {'class': 'popup-form__input input'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'popup-form__input input'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Повторите новый пароль'})


class PromoRobokassaForm(RobokassaForm):

    def __init__(self, *args, **kwargs):

        super(PromoRobokassaForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'shppromo':
                self.fields[field].widget = forms.TextInput()
                self.fields[field].widget.attrs.update(
                    {'class': 'input'})
                self.fields[field].widget.attrs.update(
                    {'placeholder': 'Промокод'})


class RobokassaPaymentMethodsForm(RobokassaForm):

    def __init__(self, *args, **kwargs):
        self.IncCurrLabel = kwargs['initial']['IncCurrLabel']
        super(RobokassaPaymentMethodsForm, self).__init__(*args, **kwargs)

        self.fields['IncCurrLabel'] = forms.ChoiceField(
            choices=getRobokassaPaymentMethods(s.ROBOKASSA_MERCHANT_LOGIN),
            widget=forms.Select(
                attrs={
                    'class': 'popup-form__input input',
                    'onchange': f"changePaymentMethodsAjax(this)"
                },
            ),
            initial=self.IncCurrLabel,
            label=False
        )


def robokassa_form(request, calc_name, redirect=f'{s.CALC_INDEX_URL}accounts/profile/', price_type='price', **kwargs):
    """Возвращает форму робокассы для оплаты
        price_type=day - за сутки использования одного калькулятора
        price_type=once - за один расчёт калькулятора
        price_type=all - за сутки использования всех калькуляторов

    returns:
        initial: {
            OutSum - Стоимость без комиссии
            InvId - Номер заказа/оплаты
            Desc - Описание для оплаты
            IncCurrLabel - Предлагаемый способ оплаты
            ...
        }

    """
    IncCurrLabel = 'BankCard'
    user = request.user
    price = None

    if 'IncCurrLabel' in kwargs:
        IncCurrLabel = kwargs['IncCurrLabel']

    if 'price' in kwargs:
        price = kwargs['price']

    # get random of two price
    # price_type = request.session['price_type']

    #если не установлено значение ДЛЯ price_type, по умолчанию - 'price' 
    price = get_chunk_value_by_name(calc_name, price_type) or \
            get_chunk_value_by_name(calc_name, 'price')

    price = 0 if price is None else float(price)
        

    order = Order.objects.filter(
        user=user,
        calc_name=calc_name,
        status=''
    ).order_by('-date').first()

    if not order:
        order = Order.objects.get_or_create(
            user=user,
            calc_name=calc_name,
            status='',
            price=price
        )[0]

    promo = None

    if order.promo:
        price -= price * int(order.promo.discount) / 100
        promo = order.promo.name

    full_price = price

    no_commission_price = getRobokassaNoCommission(
        s.ROBOKASSA_MERCHANT_LOGIN, price, IncCurrLabel)
    # payment_methods = getRobokassaPaymentMethods(s.ROBOKASSA_MERCHANT_LOGIN)
    # form_id = 'form_id_' + ''.join([str(random.randint(0, 9)) for i in range(8)])

    return RobokassaPaymentMethodsForm(
        initial={
            'OutSum': no_commission_price,
            'InvId': order.id,
            'Desc': f'Оплата по калькулятору {order.calc_name} ({price_type})',
            'IncCurrLabel': IncCurrLabel,
            'Culture': 'ru',
            'Email': '',

            # 'promo': promo,
            'calc_name': order.calc_name,
            'user': order.user,
            'redirect': redirect,
            'full_price': full_price,
            'price_type': price_type
        },
        # payment_methods=payment_methods,
        # initial_choice=IncCurrLabel,
        # form_id=form_id,
    )


def getRobokassaNoCommission(MerchantLogin, IncSum, IncCurrLabel='BankCard'):
    """Возвращает стоимость заказа без комиссии"""
    commission_url = 'https://auth.robokassa.ru/Merchant/WebService/Service.asmx/CalcOutSumm'
    params = {
        'MerchantLogin': MerchantLogin,
        'IncSum': IncSum,                   # Стоимость изначальная
        'IncCurrLabel': IncCurrLabel        # Желаемый способ оплаты
    }

    try:
        res = requests.get(commission_url, params=params)
    except ConnectionError as e:
        logger.debug("getRobokassaNoCommission ConnectionError")
        logger.debug(e)
        return False

    if res.status_code == 200:
        try:
            root = ET.fromstring(res.text)
        except:
            res.encoding = "utf-8-sig"
            root = ET.fromstring(res.text)

        for tag in root.iter():
            if 'OutSum' in tag.tag:
                return tag.text

    return False

