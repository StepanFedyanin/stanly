import os
# import re
# import subprocess
import json as JSON
# import xlsxwriter

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from mw_calc.helpers import *
from mw_calc.models import Calculation
from mw_calc.utils import *
from mw_calc.decorators import check_payment
from mw_calc.forms import StepLoginForm, StepSignupForm, robokassa_form

from django.conf import settings as s

import logging
logger = logging.getLogger('logfile')

class home_page(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        self.template_name = '{}/home.html'.format(self.calc_name)

        context = {
            'calc_name': self.calc_name
        }

        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class steps_no_auth(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        group_number = None
        isRedirect = False
        JSON_OUT_DIR = get_json_out_dir(self.calc_name)
        template_name = self.calc_name + '/'

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            context = get_steps(step, self.calc_name)

            if step == 1:
                template_name += "step_1.html"
            elif step == 2:
                group_number = 1
                set_calc_session(request, self.calc_name,
                               'group_count', group_number)
                context['group_number'] = group_number
                template_name += "step_2.html"
            elif step == 3:
                scales = get_calc_session(request, self.calc_name, 'scales')
                if scales:
                    scales = JSON.loads(scales)
                    context['scales'] = scales
                    context['group_count'] = get_calc_session(
                        request, self.calc_name, 'group_count')
                    context['group_count_range'] = range(
                        1, context['group_count'] + 1)
                    template_name += "step_3.html"
                else:
                    isRedirect = True
            # removed auth step
            # elif step == 4:
            #     order_id = request.session['order_id']

            #     if is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
            #         html_file = get_html_file(
            #             request, 'short', self.calc_name)
            #         context['html_file'] = html_file
            #         context['get_file'] = True
            #         context['login_form'] = StepLoginForm()
            #         context['signup_form'] = StepSignupForm()
            #         template_name += "step_4.html"
            #     else:
            #         isRedirect = True

        if isRedirect:
            return HttpResponseRedirect('/')

        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class steps_auth(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        isRedirect = False
        template_name = self.calc_name + '/'

        JSON_OUT_DIR = get_json_out_dir(self.calc_name)

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            order_id = request.session['order_id']
            context = get_steps(step, self.calc_name)

        # removed auth step
        # if step == 5:

        if step == 4:
            if is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
                if is_paid(request, self.calc_name):
                    context['is_paid'] = True

                context['get_file'] = True
                # context['try_it'] = get_order_param(request, self.calc_name, 'try_it')

                html_file = get_html_file(
                    request, 'middle', self.calc_name)
                context['html_file'] = html_file
                redirect = '{}{}/steps/{}/'.format(
                    s.CALC_INDEX_URL, self.calc_name, context['next_step'])

                price = get_chunk_value_by_name(self.calc_name, 'price')
                price_once = get_chunk_value_by_name(self.calc_name, 'price_once')
                price_all = get_chunk_value_by_name(self.calc_name, 'price_all')

                if price:
                    price = int(price)
                    context['pay'] = {
                        'calc_name': self.calc_name,
                        'price_type': 'price',
                        'price': price
                    }

                if price_once:
                    price_once = int(price_once)
                    context['pay_once'] = {
                        'calc_name': self.calc_name,
                        'price_type': 'price_once',
                        'price': price_once,
                        'price_old': price_once + 20
                    }

                if price_all:
                    price_all = int(price_all)
                    context['pay_all'] = {
                        'calc_name': self.calc_name,
                        'price_type': 'price_all',
                        'price': price_all
                    }

                context['robokassa_form'] = robokassa_form(
                    request,
                    self.calc_name,
                    redirect=redirect
                )
                template_name += "step_5.html"
            else:
                isRedirect = True

        if isRedirect:
            return HttpResponseRedirect('/')

        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class steps_payment(TemplateView):
    calc_name = None

    @check_payment
    def get(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        isRedirect = False
        template_name = self.calc_name + '/'

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            order_id = request.session['order_id']
            context = get_steps(step, self.calc_name)

            # removed auth step
            # if step == 6:

            if step == 5:
                JSON_OUT_DIR = get_json_out_dir(self.calc_name)

                if is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
                    html_file = get_html_file(
                        request, 'full', self.calc_name)
                    context['html_file'] = html_file
                    context['get_file'] = True
                    template_name += "step_6.html"
                    context['next_step'] = 7
                else:
                    isRedirect = True
            elif step == 7:
                template_name += "step_7.html"
                context['next_step'] = 8

        if isRedirect:
            return HttpResponseRedirect('/')

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        isRedirect = False
        template_name = self.calc_name + '/'

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            order_id = request.session['order_id']
            context = get_steps(step, self.calc_name)

            if step == 8:
                if 'file' in request.FILES:
                    file = request.FILES['file']
                    fs = OverwriteStorage()
                    fs.save('./tmp/desc/' + file.name, file)
                    JSON_OUT_DIR = get_json_out_dir(self.calc_name)

                    if is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
                        context['html_file'] = get_html_file(
                            request, 'full', self.calc_name)
                        context['desc_file'] = file.name
                        context['get_file'] = True
                        template_name += "step_8.html"
                        context['next_step'] = None
                    else:
                        isRedirect = True
                else:
                    isRedirect = True

        if isRedirect:
            return HttpResponseRedirect('/')

        return render(request, template_name, context)


def set_group_data(request):
    if request.method == "POST":
        group_number = int(get_request_param(request, 'group_number'))
        group_count = int(get_request_param(request, 'group_count'))
        group_name = get_request_param(request, 'group_name')
        calc_name = get_request_param(request, 'calc_name')
        group_data = JSON.loads(get_request_param(request, 'group_data'))
        data_error = True

        for scale in group_data:
            for key_i in group_data[scale]:
                data_error = True
                for key_j in group_data[scale]:
                    if group_data[scale][key_i] != group_data[scale][key_j]:
                        data_error = False
                        break
                if data_error:
                    return HttpResponseBadRequest(JSON.dumps({'DATA_ERROR': scale}))

        set_calc_session(request, calc_name, 'group_number', group_number)
        set_calc_session(request, calc_name, 'group_name_' +
                       str(group_number), group_name)
        set_calc_session(request, calc_name, 'group_count_' +
                       str(group_number), group_count)
        set_calc_session(request, calc_name, 'group_data_' +
                       str(group_number), group_data)

        return HttpResponse('OK')



def set_scales(request):
    if request.method == 'POST':
        scales = dict(request.POST.items())
        calc_name = scales.pop('calc_name')
        scales_list = []
        is_valid = False
        minScaleCount = 3
        currentScaleCount = 0

        for scale in scales:
            if scales[scale]:
                scales_list.append(scales[scale])
                currentScaleCount += 1

        if currentScaleCount >= minScaleCount:
            is_valid = True

        if is_valid:
            set_calc_session(request, calc_name, 'scales',
                           JSON.dumps(scales_list))
            return HttpResponse('OK')
        else:
            return HttpResponseBadRequest('ERROR')