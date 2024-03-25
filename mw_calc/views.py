import os
import re
import json as JSON
import logging
import requests
import xlsxwriter
# from collections.abc import Iterable
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core.files import File
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile
from django.conf import settings as s

# from planfix.models import PlanfixModel
# from planfix.api import PlanFix

from .models import Calculation
from .utils import *
from .helpers import *
from .decorators import check_payment
from .forms import (
    StepLoginForm,
    StepSignupForm,
    robokassa_form,
    UploadFileForm,
    RobokassaPaymentMethodsForm
)


logger = logging.getLogger('logfile')


class index(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        calcs = dict()

        for calc_name in s.CALC_NAMES:
            calcs[calc_name] = {
                'translate': s.CALC_NAMES_TRANS[calc_name],
                'url': request.path + calc_name + '/steps/1/',
                'sample_short': get_chunk_value_by_name(calc_name, 'sample_short'),
                'sample_full': get_chunk_value_by_name(calc_name, 'sample_full'),
                'video': get_chunk_value_by_name(calc_name, 'video_url'),
                'prolog_description': get_chunk_value_by_name(calc_name, 'prolog_description')
            }

        context = {
            'calcs': calcs,
        }

        return render(request, self.template_name, context)


class dogovor(TemplateView):
    template_name = "layout/dogovor.html"


def sample(request, *args, **kwargs):
    template_name = 'sample.html'
    calc_name = kwargs['calc_name']

    context = {
        'translate': s.CALC_NAMES_TRANS[calc_name],
        'sample_full': get_chunk_value_by_name(calc_name, 'sample_full'),
        'sample_short': get_chunk_value_by_name(calc_name, 'sample_short'),
    }

    return render(request, template_name, context)


class calc_home_page(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        self.template_name = 'home.html'

        context = {
            'calc_name': self.calc_name
        }

        return render(request, self.template_name, context)

@csrf_exempt
def achievement_close(request):
    if request.method == 'POST':
        request.session['achievement_close'] = True
        return HttpResponse('OK')

@csrf_exempt
def get_video(request):
    if request.method == 'POST':
        template_name = 'ajax/get_video.html'
        calc_name = get_request_param(request, "calc_name")
        video = get_chunk_value_by_name(calc_name, 'video_url')
        context = {
            'video': video,
            'calc_name': calc_name,
            'translate': s.CALC_NAMES_TRANS[calc_name],
        }
        return render(request, template_name, context)

@csrf_exempt
def get_sample(request):
    if request.method == 'POST':
        template_name = 'ajax/get_sample.html'
        calc_name = get_request_param(request, "calc_name")
        sample_short = get_chunk_value_by_name(calc_name, 'sample_short')
        sample_full = get_chunk_value_by_name(calc_name, 'sample_full')
        context = {
            'calc_name': calc_name,
            'sample_short': sample_short,
            'sample_full': sample_full
        }
        return render(request, template_name, context)

@csrf_exempt
def get_full_example(request):
    if request.method == 'POST':
        template_name = 'ajax/get_full_example.html'
        calc_name = get_request_param(request, "calc_name")
        full_example = get_chunk_value_by_name(calc_name, 'full_example')
        context = {
            'calc_name': calc_name,
            'full_example': full_example,
        }
        return render(request, template_name, context)

@method_decorator(login_required, name='dispatch')
class calc_steps_no_auth(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        group_number = None
        isRedirect = False
        JSON_OUT_DIR = get_json_out_dir(self.calc_name)

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            context = get_steps(step, self.calc_name)

            if step == 1:
                template_name = "step_1.html"
            elif step in (2, 3):

                if step == 2:
                    group_number = 1
                else:
                    group_number = 2

                set_calc_session(request, self.calc_name,
                               'group_count', group_number)
                context['group_number'] = group_number
                template_name = "step_2_3.html"
            elif step == 4:
                scales = JSON.loads(get_calc_session(
                    request, self.calc_name, 'scales'))
                context['scales'] = scales
                context['group_count'] = get_calc_session(
                    request, self.calc_name, 'group_count')
                context['group_count_range'] = range(
                    1, context['group_count'] + 1)
                template_name = "step_4.html"

        if isRedirect:
            return HttpResponseRedirect('/')

        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class calc_steps_auth(TemplateView):
    calc_name = None

    def get(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])

        # calc_name = self.calc_name
        # if 'correlation_name' in self.kwargs:
        #     calc_name = self.kwargs['correlation_name']

        isRedirect = False

        JSON_OUT_DIR = get_json_out_dir(self.calc_name)

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            order_id = request.session['order_id']
            context = get_steps(step, self.calc_name)

        if step == 5:
            if is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
                context['no_pay'] = check_no_pay(request, self.calc_name)
                context['is_paid'] = is_paid(request, self.calc_name)
                context['get_file'] = True
                context['html_file'] = get_html_file(
                    request, 'middle', self.calc_name)

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

                template_name = "step_5.html"
            else:
                isRedirect = True

        if isRedirect:
            return HttpResponseRedirect('/')

        return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class calc_steps_payment(TemplateView):
    calc_name = None

    @check_payment
    def get(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        isRedirect = False

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            order_id = request.session['order_id']
            context = get_steps(step, self.calc_name)

            if step == 6:
                JSON_OUT_DIR = get_json_out_dir(self.calc_name)

                if is_file_exist(os.path.join(JSON_OUT_DIR, (order_id + '.json'))):
                    context['html_file'] = get_html_file(
                        request, 'full', self.calc_name)
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

        expire_count_decrement(request, self.calc_name)
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        step = int(self.kwargs['step'])
        isRedirect = False
        context = get_steps(step, self.calc_name)

        if 'order_id' not in request.session or not request.session['order_id']:
            isRedirect = True
        else:
            order_id = request.session['order_id']
            context = get_steps(step, self.calc_name)

            if step == 9:
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
                        template_name = "step_8.html"
                        context['next_step'] = None
                    else:
                        isRedirect = True
                else:
                    isRedirect = True

        if isRedirect:
            return HttpResponseRedirect('/')

        return render(request, template_name, context)


def calc_set_scales(request):
    if request.method == 'POST':
        scales = dict(request.POST.items())
        if 'calc_name' not in scales:
            return HttpResponseRedirect()
        calc_name = scales.pop('calc_name')
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

        if is_valid:
            set_calc_session(request, calc_name, 'scales',
                           JSON.dumps(scales_list))
            return HttpResponse('OK')
        else:
            return HttpResponseBadRequest('ERROR')


def calc_set_json(request):
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


def calc_get_group_inputs(request):
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


def calc_set_group_data(request, calc_name=None):
    if request.method == "POST":
        params = dict(request.POST.items())
        group_number = int(params['group_number'])
        group_count = int(params['group_count'])
        group_name = params['group_name']
        calc_name = params['calc_name']
        group_data = JSON.loads(params['group_data'])

        set_calc_session(request, calc_name, 'group_number', group_number)
        set_calc_session(request, calc_name, 'group_name_' +
                       str(group_number), group_name)
        set_calc_session(request, calc_name, 'group_count_' +
                       str(group_number), group_count)
        set_calc_session(request, calc_name, 'group_data_' +
                       str(group_number), group_data)

        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest('ERROR')


def calc_send_xlsx(request):
    if request.method == 'POST':
        style = get_request_param(request, "action")
        email = get_request_param(request, "email")

        if not (email and re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email)):
            return HttpResponseBadRequest('email')

        xlsx_file = create_xlsx(request)
        order_id = request.session['order_id']

        send(
            s.EMAIL_HOST_USER,
            [email],  # [email, s.EMAIL_HOST_USER],
            'Результаты расчёта на сайте stanly.statpsy.ru №' + order_id,
            xlsx_file
        )

        return HttpResponse('OK')


def calc_send_docx(request):
    if request.method == 'POST':
        email = get_request_param(request, "email")

        if not (email and re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email)):
            return HttpResponseBadRequest('email')

        order_id = request.session['order_id']

        docx_file = create_docx(request)

        send(
            s.EMAIL_HOST_USER,
            [email],  # [email, s.EMAIL_HOST_USER],
            'Результаты расчёта на сайте stanly.statpsy.ru №' + order_id,
            docx_file
        )

        return HttpResponse('OK')


@csrf_exempt
def g_captcha(request):
    if request.method == 'POST':

        params = dict(request.POST.items())

        if 'token' in params:
            g_res = get_g_recaptcha(params['token'])

            if g_res['success'] and g_res['action'] == 'statpsy':
                pass
            else:
                return HttpResponseRedirect('/')

        return HttpResponse('OK')


# TODO
# Закрыть от скачивания для неоплаченных заказов
def calc_get_file(request):
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


def calc_upload_scales(request):
    if request.method == 'POST':
        redirect_to = get_request_param(request, 'redirect_to')
        calc_name = get_request_param(request, 'calc_name')

        if 'file' not in request.FILES:
            response = HttpResponseBadRequest('file uploading error')

        else:
            scales_list = handle_scales_file(request.FILES['file'])
            scales_json = JSON.dumps(scales_list)
            set_calc_session(request, calc_name, 'scales', scales_json)

            if request.is_ajax():
                response = HttpResponse(scales_json)
            else:
                response = HttpResponseRedirect(redirect_to)

        return response


def calc_upload_group(request):
    if request.method == 'POST':
        redirect_to = get_request_param(request, 'redirect_to', '')

        if 'file' not in request.FILES:
            response = HttpResponseBadRequest('file uploading error')

        else:
            # group = get_request_param(request, 'group')
            group_list = handle_group_file(request.FILES['file'])
            group_json = JSON.dumps(group_list)

            if request.is_ajax():
                response = HttpResponse(group_json)
            else:
                response = HttpResponseRedirect(redirect_to)

        return response


def calc_upload_desc(request):
    if request.method == 'POST' and 'file' in request.FILES:
        redirect_to = get_request_param(request, 'redirect_to', '')

        file = request.FILES['file']
        fs = FileSystemStorage()
        # filename = fs.save(file.name, file)
        filename = fs.save('./tmp/desc.xlsx', file)
        uploaded_file_url = fs.url(filename)

        # model_file = File(file)
        # model_file.save('./tmp/desc.xlsx', file.readlines(), True)

        response = HttpResponseRedirect(
            '{0}?file={1}'.format(redirect_to, uploaded_file_url))
    else:
        response = HttpResponseBadRequest('file uploading error')

    return response


def calc_get_xlsx_template(request):
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


def tilda_get_pages(request):
    request_params = dict(request.GET.items())
    publickey = get_request_param(
        request, 'publickey', default=s.TILDA_PUBLIC_KEY)
    pageid = get_request_param(request, 'pageid', s.TILDA_PAGE_ID)
    # ,projectid,published,

    if publickey != s.TILDA_PUBLIC_KEY and not pageid:
        return HttpResponse(False)

    tilda_api_url = s.TILDA_API_URL

    # only index.html now
    if pageid == s.TILDA_PAGE_ID:
        page_name = 'index'
    # elif pageid == s.TILDA_HEADER_PAGE_ID:
    #     page_name = 'header'
    #     tilda_api_url = "http://api.tildacdn.info/v1/getpageexport/"
    else:
        return HttpResponse(False)
        # page_name = params['pageid']

    params = {
        'publickey': s.TILDA_PUBLIC_KEY,
        'secretkey': s.TILDA_SECRET_KEY,
        'pageid': pageid,
    }

    res = requests.get(tilda_api_url, params)
    json_answer = res.json()

    return HttpResponse('ok')

    for image in json_answer["result"]["images"]:
        tilda_save_file(image["from"], image["to"], 'i')

    for image in json_answer["result"]["css"]:
        tilda_save_file(image["from"], image["to"], 'css')

    for image in json_answer["result"]["js"]:
        tilda_save_file(image["from"], image["to"], 'js')

    html = "{% load static %}" + re.sub(
        r"(tilda\/((js)|(css)|(i))\/[^\"\'\?]*)",
        "{% static '\g<1>' %}",
        json_answer["result"]["html"]
    )  # get all static files from "{% load static %}"

    path = '{}{}.html'.format(s.TILDA_TEMPLATES_ROOT, page_name)

    if(is_file_exist(path)):
        os.remove(path)

    location = default_storage.save(path, ContentFile(html))

    return HttpResponse('ok')


def tilda_save_file(url, filename, filetype):
    path = '{}/{}/{}'.format(s.TILDA_STATIC_ROOT, filetype, filename)

    if not is_file_exist(path):
        response = requests.get(url, stream=True)
        temp = NamedTemporaryFile(delete=True)
        temp.write(response.content)
        temp.flush()

        file = File(temp)
        location = default_storage.save(path, file)


def get_payment_form_ajax(request, *args, **kwargs):
    if request.POST:
        calc_name = get_request_param(request, 'calc_name')
        IncCurrLabel = get_request_param(request, 'IncCurrLabel')
        price_type = get_request_param(request, 'price_type')
        template_name = 'ajax/robokassa_hidden.html'

        form = robokassa_form(
            request,
            calc_name,
            price_type=price_type,
            IncCurrLabel=IncCurrLabel,
        )

        context = {
            'form': form
        }

        response = render(request, template_name, context)

        return response

def get_payment_methods_ajax(request, *args, **kwargs):
    if request.POST:
        template_name = 'ajax/payment_methods.html'

        context = {
            'calc_name': get_request_param(request, 'calc_name'),
            'price_type': get_request_param(request, 'price_type', 'price'),
            'payment_methods': getRobokassaPaymentMethods(s.ROBOKASSA_MERCHANT_LOGIN),
            'IncCurrLabel': get_request_param(request, 'IncCurrLabel', 'BankCard')
        }

        response = render(request, template_name, context)

        return response

def session_clear(request, *args, **kwargs):
    if request.method == 'POST':
        print('clearStorage')
        del_session_keys(request)
        return HttpResponse('session clear')
