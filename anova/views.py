import os
# import re
# import subprocess
import json as JSON
# import xlsxwriter

from django.shortcuts import render
from django.views.generic import TemplateView
# from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from mw_calc.utils import *
from mw_calc.helpers import *
from mw_calc.decorators import check_payment
from mw_calc.forms import StepLoginForm, StepSignupForm, robokassa_form

# from django.conf import settings as s

import logging
logger = logging.getLogger('logfile')


@method_decorator(login_required, name='dispatch')
class Scales(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        if 'order_id' not in request.session or not request.session['order_id']:
            return HttpResponseRedirect('/')

        step = int(self.kwargs['step'])
        context = get_steps(step, self.calc_name)
        template_name = 'step_1.html'

        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class Groups(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        if 'order_id' not in request.session or not request.session['order_id']:
            return HttpResponseRedirect('/')

        step = int(self.kwargs['step'])
        group_number = int(self.kwargs['group'])
        context = get_steps(step, self.calc_name)
        context['group_number'] = group_number
        context['group_quantity'] = get_calc_session(request, self.calc_name, 'group_quantity')
        template_name = 'step_2_3.html'

        set_calc_session(request, self.calc_name, 'group_count', group_number)

        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class Prepare(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        is_redirect = False

        if 'order_id' not in request.session or not request.session['order_id']:
            is_redirect = True
        else:
            step = int(self.kwargs['step'])
            context = get_steps(step, self.calc_name)
            template_name = 'step_4.html'
            scales = get_calc_session(request, self.calc_name, 'scales')
            if scales:
                scales = JSON.loads(scales)
                context['scales'] = scales
                context['group_count'] = get_calc_session(
                    request, self.calc_name, 'group_count')
                context['group_count_range'] = range(1, context['group_count'] + 1)
            else:
                is_redirect = True


        if is_redirect:
            return HttpResponseRedirect('/')
    
        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class Auth(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        if 'order_id' not in request.session or not request.session['order_id']:
            return HttpResponseRedirect('/')

        step = int(self.kwargs['step'])
        context = get_steps(step, self.calc_name)
        template_name = 'step_5.html'
        JSON_OUT_DIR = get_json_out_dir(self.calc_name)

        order_id = request.session['order_id']

        if not is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
            return HttpResponseRedirect('/')

        context['is_paid'] = is_paid(request, self.calc_name)
        context['get_file'] = True
        context['html_file'] = get_html_file(request, 'middle', self.calc_name)
        redirect = '{}{}/steps/{}/'.format(s.CALC_INDEX_URL,
                                           self.calc_name, context['next_step'])

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

        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class Pay(TemplateView):
    calc_name = None

    @check_payment
    def get(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])

        if 'order_id' not in request.session or not request.session['order_id']:
            return HttpResponseRedirect('/')

        template_name = ''
        context = get_context_many_groups(step, self.calc_name)
        order_id = request.session['order_id']
        JSON_OUT_DIR = get_json_out_dir(self.calc_name)

        if not is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
            return HttpResponseRedirect('/')

        context['html_file'] = get_html_file(request, 'full', self.calc_name)
        context['get_file'] = True

        template_name += "step_6.html"

        if step == 7:
            template_name = "step_7.html"

        expire_count_decrement(request, self.calc_name)
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        if 'order_id' not in request.session or not request.session['order_id']:
            return HttpResponseRedirect('/')

        order_id = request.session['order_id']
        context = get_context_many_groups(request)

        if 'file' in request.FILES:
            file = request.FILES['file']
            fs = OverwriteStorage()
            fs.save('./tmp/desc/' + file.name, file)
            JSON_OUT_DIR = get_json_out_dir(self.calc_name)

        if not is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
            return HttpResponseRedirect('/')

        context['html_file'] = get_html_file(request, 'full', self.calc_name)
        context['desc_file'] = file.name
        context['get_file'] = True
        template_name = "step_8.html"
        context['next_step'] = None

        return render(request, template_name, context)


def SetScales(request):
    if request.method == 'POST':
        scales = dict(request.POST.items())
        calc_name = scales.pop('calc_name')
        group_quantity = scales.pop('group_quantity')  # количество групп
        scales_list = []
        is_valid = False
        minScaleCount = 1
        currentScaleCount = 0

        for scale in scales:
            if scales[scale]:
                scales_list.append(scales[scale])
                currentScaleCount += 1

        if currentScaleCount >= minScaleCount:
            is_valid = True

        try:
            group_quantity = int(group_quantity)
        except ValueError:
            return HttpResponseBadRequest('QUANTITY')

        if group_quantity < 3:
            return HttpResponseBadRequest('QUANTITY')

        if not is_valid:
            return HttpResponseBadRequest('ERROR')

        set_calc_session(request, calc_name, 'group_quantity', group_quantity)
        set_calc_session(request, calc_name, 'scales', JSON.dumps(scales_list))
        return HttpResponse('OK')


def GetGroupInputs(request):
    if request.method == "POST":
        template_name = "get_group_inputs.html"
        context = get_context_many_groups(request)

        return render(request, template_name, context)


def GetFile(request):
    calc_name = get_request_param(request, 'calc_name')
    style = get_request_param(request, 'style', 'short')
    order_id = get_request_param(request, 'order_id')
    desc_file = get_request_param(request, 'desc_file')

    if not order_id:
        order_id = request.session['order_id']

    if style or calc_name:
        if style in ("short", "full"):
            filename = style + '_' + order_id + '.xlsx'
            file = os.path.join(get_xlsx_out_dir(calc_name), filename)
            # if not is_file_exist(file):
            file = create_xlsx(request)
            content_type = s.MIME_XLSX
        elif style == "docx":
            filename = order_id + '.docx'

            if desc_file:
                filename = 'desc_' + filename

            file = os.path.join(get_docx_out_dir(calc_name), filename)
            # if not is_file_exist(file):
            file = create_docx(request)
            content_type = s.MIME_DOCX

        response = HttpResponse(open(file, 'rb').read())
        response['Content-Type'] = content_type
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            filename)
        return response
    else:
        return HttpResponseBadRequest('request params error')
