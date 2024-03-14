import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core import serializers

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from mw_calc import settings as s
from mw_calc.helpers import del_session_keys, get_chunk_value_by_name
from mw_calc.utils import get_request_param
from mw_calc.forms import robokassa_form
from mw_calc.decorators import get_calcs, _get_calc_context
from mw_calc.models import Order, Calculation
from mw_calc.forms import (
    ProfileLoginForm,
    ProfileSignupForm,
    ProfileAddEmailForm,
    ProfileResetPasswordForm,
    ProfileResetPasswordKeyForm,
    AjaxSignupForm,
    AjaxLoginForm,
    AjaxResetPasswordForm,
)

from allauth.account.views import (
    LoginView,
    SignupView,
    _ajax_response,
    EmailView,
    PasswordResetView,
    PasswordResetDoneView,
    EmailVerificationSentView,
    PasswordResetFromKeyView
)
from allauth.account import app_settings

from .helpers import random_promo, is_promo
from .utils import get_promo_by_user
from .models import Promo

logger = logging.getLogger('logfile')


@login_required
@get_calcs
def profile(request, *args, **kwargs):
    template_name = 'lk/profile.html'

    context = {
        "calcs": kwargs['calcs']
    }

    # promo = get_promo_by_user(request.user)
    # logger(context)

    # if promo:
        # context['promo'] = promo

    return render(request, template_name, context)


@login_required
def promo(request, *args, **kwargs):
    template_name = 'lk/promo.html'
    context = dict()
    promo = get_promo_by_user(request.user)
    if promo:
        context['promo'] = promo

    return render(request, template_name, context)


@login_required
@get_calcs
def history_list(request, *args, **kwargs):
    template_name = 'lk/history_list.html'

    context = {
        "calcs": kwargs['calcs']
    }

    price_all = get_chunk_value_by_name('mann_whitney', 'price_all')

    context['pay'] = {
        'calc_name': 'mann_whitney',
        'price_type': 'price_all',
        'price': price_all
    }

    return render(request, template_name, context)


@login_required
def history(request, *args, **kwargs):
    template_name = 'lk/history.html'
    context = dict()
    calc_name = kwargs['calc_name']
    calc = _get_calc_context(request, calc_name)

    price = get_chunk_value_by_name(calc_name, 'price')
    context['pay'] = {
        'calc_name': calc_name,
        'price_type': 'price',
        'price': price
    }
    context['calc'] = calc[calc_name]
    return render(request, template_name, context)


def clear(request, *args, **kwargs):
    del_session_keys(request)
    return HttpResponseRedirect('/')


class AjaxSignupView(SignupView):
    form_class = AjaxSignupForm
    template_name = "account/signup_ajax." + app_settings.TEMPLATE_EXTENSION

    def get(self, request, *args, **kwargs):
        response = super(AjaxSignupView, self).get(
            request, *args, **kwargs)
        form = self.get_form()
        return _ajax_response(
            self.request, response, form=form, data=self._get_ajax_data_if())

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            response = self.form_valid(form)
            return _ajax_response(
                self.request, response, form=form, data=self._get_ajax_data_if())
        else:
            return JsonResponse({'errors': form.errors})


class AjaxLoginView(LoginView):
    form_class = AjaxLoginForm
    template_name = "account/login_ajax." + app_settings.TEMPLATE_EXTENSION

    def get(self, request, *args, **kwargs):
        response = super(AjaxLoginView, self).get(
            request, *args, **kwargs)
        form = self.get_form()
        return _ajax_response(
            self.request, response, form=form, data=self._get_ajax_data_if())

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            response = self.form_valid(form)
            return _ajax_response(
                self.request, response, form=form, data=self._get_ajax_data_if())
        else:
            return JsonResponse({'errors': form.errors})


class AjaxPasswordResetView(PasswordResetView):
    form_class = AjaxResetPasswordForm
    template_name = "account/reset_password_ajax." + app_settings.TEMPLATE_EXTENSION

    def get(self, request, *args, **kwargs):
        response = super(AjaxPasswordResetView, self).get(
            request, *args, **kwargs)
        form = self.get_form()
        return _ajax_response(
            self.request, response, form=form, data=self._get_ajax_data_if())

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            response = self.form_valid(form)
            res = _ajax_response(
                self.request, response, form=form, data=self._get_ajax_data_if())
            return res
        else:
            return JsonResponse({'errors': form.errors})


class AjaxPasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/reset_password_done_ajax." + app_settings.TEMPLATE_EXTENSION


class AjaxEmailVerificationSentView(EmailVerificationSentView):
    template_name = "account/verification_sent_ajax." + app_settings.TEMPLATE_EXTENSION


class ProfileEmailVerificationSentView(EmailVerificationSentView):
    template_name = (
        'account/verification_sent.' + app_settings.TEMPLATE_EXTENSION)

class ProfileLoginView(LoginView):
    form_class = ProfileLoginForm
    template_name = "account/login." + app_settings.TEMPLATE_EXTENSION


class ProfileSignupView(SignupView):
    form_class = ProfileSignupForm
    template_name = "account/signup." + app_settings.TEMPLATE_EXTENSION


class ProfileEmailView(EmailView):
    form_class = ProfileAddEmailForm


class ProfilePasswordResetView(PasswordResetView):
    form_class = ProfileResetPasswordForm


class ProfilePasswordResetFromKeyView(PasswordResetFromKeyView):
    form_class = ProfileResetPasswordKeyForm


def create_promo(request, *args, **kwargs):
    if request.POST:
        params = dict(request.POST.items())
        promo = params['promo']

        if is_promo(promo):
            user = request.user

            try:
                promo_obj = Promo.objects.create(
                    name=promo,
                    user=user,
                    active=True,
                    private=False,
                    expire=timezone.now() + timezone.timedelta(days=365)
                )

                response = HttpResponse('OK')
            except IntegrityError:
                response = HttpResponseBadRequest('EXIST')
        else:
            response = HttpResponseBadRequest('ERROR')

        return response


def delete_promo(request, *args, **kwargs):
    if request.POST:
        params = dict(request.POST.items())
        promo = params['promo']

        user = request.user

        try:
            promo_obj = Promo.objects.get(
                name=promo,
                user=user
            )

            promo_obj.delete()
            response = HttpResponse('OK')

        except Promo.DoesNotExist:
            response = HttpResponseBadRequest('NOT EXIST')

        return response


def apply_promo(request, *args, **kwargs):
    if request.POST:
        promo = get_request_param(request, 'promo')
        calc_name = get_request_param(request, 'calc_name')
        user = request.user
        template_name = 'block/robokassa.html'
        context = {}

        # Если существует промокод для этого пользователя
        try:
            promo_obj = Promo.objects.get(
                Q(name=promo, active=True, expire__gt=timezone.now())
            )

        except Promo.DoesNotExist:
            response = HttpResponseBadRequest('NOT EXIST')

        else:
            # Промокод private - может использовать этот пользователь
            if promo_obj.private and promo_obj.user == user:
                # Если пользователь ещё не использовал этот промокод

                
                # order_obj = Order.objects.filter(
                #     Q(user=user, promo=promo_obj)
                # ).order_by('date').last()
                # print(order_obj)
                # if order_obj:
                #     response = HttpResponseBadRequest('USED')
                # else:
                #     order_obj = Order.objects.filter(
                #         Q(user=user, calc_name=calc_name)
                #     ).order_by('date').last()
                #     print(order_obj)

                #     order_obj.promo = promo_obj
                #     order_obj.save(update_fields=['promo'])

                    response = render(request, template_name, context)
            # Промокод public - может использовать другой пользователь
            elif not promo_obj.private and promo_obj.user != user:
                # Если пользователь ещё не использовал этот промокод
                order_obj = Order.objects.filter(
                    Q(user=user, promo=promo_obj)
                ).order_by('date').last()

                if order_obj:
                    response = HttpResponseBadRequest('USED')
                else:
                    # order_obj = Order.objects.filter(
                    #     Q(user=user, calc_name=calc_name)
                    # ).order_by('date').last()
                    # print(order_obj)

                    # order_obj.promo = promo_obj
                    # order_obj.save(update_fields=['promo'])

                    # Promo.objects.create(
                    #     name=random_promo(),
                    #     user=promo_obj.user,
                    #     active=True,
                    #     private=True,
                    #     expire=timezone.now() + timezone.timedelta(days=365)
                    # )

                    response = render(request, template_name, context)
            else:
                response = HttpResponseBadRequest('NOT EXIST')

        return response
