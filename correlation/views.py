import os
import json as JSON
import xlsxwriter

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
        correlation_name = self.kwargs['correlation_name']
        self.template_name = 'home.html'.format(self.calc_name)

        context = {
            'calc_name': correlation_name
        }

        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class steps_no_auth(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        correlation_name = self.kwargs['correlation_name']
        group_number = None
        isRedirect = False
        JSON_OUT_DIR = get_json_out_dir(correlation_name)

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            context = get_steps(step, correlation_name)

            if step == 1:
                template_name = "step_1.html"

            elif step == 2:
                group_number = 1
                set_calc_session(request, correlation_name,
                               'group_count', group_number)
                context['group_number'] = group_number
                template_name = "step_2_3.html"

            elif step == 3:
                scales = get_calc_session(request, correlation_name, 'scales')
                if scales:
                    scales = JSON.loads(scales)
                    context['scales'] = scales
                    context['group_count'] = get_calc_session(
                        request, correlation_name, 'group_count')
                    context['group_count_range'] = range(
                        1, context['group_count'] + 1)
                    template_name = "step_4.html"
                else:
                    isRedirect = True

        if isRedirect:
            return HttpResponseRedirect('/')

        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class steps_auth(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        isRedirect = False
        correlation_name = self.kwargs['correlation_name']

        JSON_OUT_DIR = get_json_out_dir(correlation_name)

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            order_id = request.session['order_id']
            context = get_steps(step, correlation_name)

            if step == 4:
                if is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
                    if is_paid(request, correlation_name):
                        context['is_paid'] = True

                    context['get_file'] = True
                    # context['try_it'] = get_order_param(request, correlation_name, 'try_it')

                    html_file = correlation_get_html_file(
                        request, 'middle', correlation_name)
                    context['html_file'] = html_file
                    redirect = '{}{}/steps/{}/'.format(
                        s.CALC_INDEX_URL, correlation_name, context['next_step'])

                    price = get_chunk_value_by_name(correlation_name, 'price')
                    price_once = get_chunk_value_by_name(correlation_name, 'price_once')
                    price_all = get_chunk_value_by_name(correlation_name, 'price_all')

                    if price:
                        price = int(price)
                        context['pay'] = {
                            'calc_name': correlation_name,
                            'price_type': 'price',
                            'price': price
                        }

                    if price_once:
                        price_once = int(price_once)
                        context['pay_once'] = {
                            'calc_name': correlation_name,
                            'price_type': 'price_once',
                            'price': price_once,
                            'price_old': price_once + 20
                        }

                    if price_all:
                        price_all = int(price_all)
                        context['pay_all'] = {
                            'calc_name': correlation_name,
                            'price_type': 'price_all',
                            'price': price_all
                        }

                    template_name = "step_5.html"
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
        correlation_name = self.kwargs['correlation_name']

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            order_id = request.session['order_id']
            context = get_steps(step, correlation_name)

            if step == 5:
                JSON_OUT_DIR = get_json_out_dir(correlation_name)

                if is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
                    html_file = correlation_get_html_file(
                        request, 'full', correlation_name)
                    context['html_file'] = html_file
                    context['get_file'] = True
                    template_name = "step_6.html"
                    context['next_step'] = 7
                else:
                    isRedirect = True
            elif step == 7:
                template_name = "step_7.html"
                context['next_step'] = 8

        if isRedirect:
            return HttpResponseRedirect('/')

        expire_count_decrement(request, correlation_name)
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        isRedirect = False

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            correlation_name = self.kwargs['correlation_name']
            order_id = request.session['order_id']
            context = get_steps(step, correlation_name)

            if step == 8:
                if 'file' in request.FILES:
                    file = request.FILES['file']
                    fs = OverwriteStorage()
                    fs.save('./tmp/desc/' + file.name, file)
                    JSON_OUT_DIR = get_json_out_dir(correlation_name)

                    if is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
                        context['html_file'] = correlation_get_html_file(
                            request, 'full', correlation_name)
                        context['desc_file'] = file.name
                        context['get_file'] = True
                        template_name = "step_8.html"
                        context['next_step'] = None
                    else:
                        isRedirect = True
                else:
                    isRedirect = True

        if isRedirect:
            return HttpResponseRedirect('/')

        return render(request, template_name, context)


def set_scales(request, correlation_name=None):
    if request.method == 'POST':
        scales = dict(request.POST.items())
        correlation_name = scales.pop('calc_name')
        scales_list = []
        is_valid = False
        minScaleCount = 2
        currentScaleCount = 0

        for scale in scales:
            if scales[scale]:
                scales_list.append(scales[scale])
                currentScaleCount += 1

        if currentScaleCount >= minScaleCount:
            is_valid = True

        if is_valid:
            set_calc_session(request, correlation_name,
                           'scales', JSON.dumps(scales_list))
            return HttpResponse('OK')
        else:
            return HttpResponseBadRequest('ERROR')


def set_group_data(request, correlation_name=None):
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


def get_file(request, correlation_name=None):
    calc_name = get_request_param(request, 'calc_name')
    style = get_request_param(request, 'style', 'short')
    order_id = get_request_param(request, 'order_id')
    desc_file = get_request_param(request, 'desc_file')

    if not order_id:
        order_id = request.session['order_id']

    if not style or not calc_name:
        return HttpResponseBadRequest('request params error')
    else:

        if style in ("short", "full"):
            filename = style + '_' + order_id + '.xlsx'
            file = os.path.join(get_xlsx_out_dir(correlation_name), filename)
            # if not is_file_exist(file):
            file = correlation_create_xlsx(request)
            content_type = s.MIME_XLSX
        elif style == "docx":
            filename = order_id + '.docx'

            if desc_file:
                filename = 'desc_' + filename

            file = os.path.join(get_docx_out_dir(correlation_name), filename)
            # if not is_file_exist(file):
            file = correlation_create_docx(request)
            content_type = s.MIME_DOCX

        response = HttpResponse(open(file, 'rb').read())
        response['Content-Type'] = content_type
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            filename)

        return response


def get_group_inputs(request, correlation_name=None):
    if request.method == "POST":
        calc_name = get_request_param(request, 'calc_name')
        scales = get_calc_session(request, calc_name, 'scales')

        if scales:
            scales = JSON.loads(scales)
            step = int(get_request_param(request, 'step'))
            group_number = int(get_request_param(request, 'group_number'))
            group_count = int(get_request_param(request, 'group_count'))
            group_name = get_request_param(request, 'group_name')
            template_name = "get_group_inputs.html"

            return render(request, template_name, {
                'scales': scales,
                'calc_name': calc_name,
                'step': step,
                'prev_step': step - 1,
                'next_step': step + 1,
                'group_name': group_name,
                'group_count_range': range(1, group_count + 1),
                'group_count': group_count,
                'group_number': group_number,
            })
        else:
            return HttpResponseBadRequest('NO_SCALES')

    return HttpResponseBadRequest('ERROR')


def get_xlsx_template(request, correlation_name=None):
    calc_name = get_request_param(request, 'calc_name')

    xlsx_template = os.path.join(
        get_xlsx_out_dir(calc_name), ('template.xlsx'))

    workbook = xlsxwriter.Workbook(xlsx_template)
    worksheet = workbook.add_worksheet()

    scales = JSON.loads(get_calc_session(request, calc_name, 'scales'))

    for scale, i in zip(scales, range(0, len(scales))):
        worksheet.write(0, i, scale)

    workbook.close()

    content_type = s.MIME_XLSX
    response = HttpResponse(open(xlsx_template, 'rb').read())
    response['Content-Type'] = content_type
    response['Content-Disposition'] = 'attachment; filename="template.xlsx"'

    return response


def set_json(request, correlation_name=None):
    if request.method == "POST":
        calc_name = get_request_param(request, "calc_name")
        order_id = request.session['order_id']

        JSON_OUT_DIR = get_json_out_dir(calc_name)
        json_file = os.path.join(JSON_OUT_DIR, (order_id + '.json'))
        json_req = get_request_param(request, 'json')

        set_calc_session(request, calc_name, 'req', json_req)

        f = open(json_file, "w")
        f.write(json_req)
        f.close()

        if request.user.is_authenticated:
            Calculation.objects.get_or_create(
                order_id=order_id,
                user=request.user,
                calc_name=calc_name
            )

        return HttpResponse("OK")


def correlation_get_html_file(request, html_format, calc_name, correlation_name=None):
    correlation_name = correlation_check(calc_name)
    HTML_OUT_DIR = get_html_out_dir(calc_name)
    SCRIPT_DIR = get_script_dir(correlation_name)
    desc_file = get_request_param(request, 'desc_file')

    order_id = request.session['order_id']
    # json_file = request.session['json_file']
    JSON_OUT_DIR = get_json_out_dir(calc_name)
    json_file = os.path.join(JSON_OUT_DIR, (order_id + '.json'))
    html_file = calc_name + '_' + html_format + '_' + order_id + '.html'
    script = os.path.join(SCRIPT_DIR, s.HTML_SCRIPT)

    if 'file' in request.FILES:
        desc_file = request.FILES['file']

    # remove before creation
    if is_file_exist(HTML_OUT_DIR + html_file):
        os.remove(HTML_OUT_DIR + html_file)

    result = rmd_script(s.HOME_DIR, script, HTML_OUT_DIR, html_file,
               json_file, html_format, desc_file,
               calc_name=calc_name)

    if result:
        return html_file
    else:
        logger.debug(
            'correlation_get_html_file',
            html_file,
            json_file
        )
        return False


def correlation_create_docx(request, correlation_name=None):
    calc_name = get_request_param(request, 'calc_name')
    order_id = get_request_param(request, 'order_id')
    desc_file = get_request_param(request, 'desc_file')
    correlation_name = correlation_check(calc_name)

    if not order_id:
        order_id = request.session['order_id']

    JSON_OUT_DIR = get_json_out_dir(calc_name)
    json_file = os.path.join(JSON_OUT_DIR, (order_id + '.json'))

    if not is_file_exist(json_file):
        return HttpResponseBadRequest('no json file')

    filename = order_id + '.docx'

    if desc_file:
        filename = 'desc_' + filename

    DOCX_OUT_DIR = get_docx_out_dir(calc_name)
    SCRIPT_DIR = get_script_dir(correlation_name)
    docx_file = os.path.join(DOCX_OUT_DIR, filename)
    script = os.path.join(SCRIPT_DIR, s.DOCX_SCRIPT)
    rmd_script(s.HOME_DIR, script, DOCX_OUT_DIR,
               docx_file, json_file, 'docx', desc_file,
               calc_name=calc_name)

    return docx_file


def correlation_create_xlsx(request, correlation_name=None):
    calc_name = get_request_param(request, 'calc_name')
    correlation_name = correlation_check(calc_name)
    order_id = get_request_param(request, 'order_id')
    style = get_request_param(request, 'style', 'short')

    if not order_id:
        order_id = request.session['order_id']

    XLSX_OUT_DIR = get_xlsx_out_dir(calc_name)
    SCRIPT_DIR = get_script_dir(correlation_name)
    XLSX_SCRIPT = s.XLSX_SCRIPT
    script_file = os.path.join(SCRIPT_DIR, XLSX_SCRIPT)

    JSON_OUT_DIR = get_json_out_dir(calc_name)
    json_file = os.path.join(JSON_OUT_DIR, (order_id + '.json'))

    if not is_file_exist(json_file):
        return HttpResponseBadRequest('no json file')

    xlsx_file = os.path.join(XLSX_OUT_DIR, (style + '_' + order_id + '.xlsx'))
    r_script(script_file, json_file, xlsx_file, style, calc_name=calc_name)

    return xlsx_file


def correlation_check(calc_name, correlation_name=None):
    if calc_name in ("correlation_spearman", "correlation_pearson", "correlation_kendall"):
        correlation_name = "correlation"
    else:
        correlation_name = calc_name

    return correlation_name
