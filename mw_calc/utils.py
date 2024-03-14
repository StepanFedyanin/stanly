"""Summary

Attributes:

"""

import os
import time
import pandas as pd
import logging
import subprocess
import requests
import json as JSON
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.conf import settings as s
from django.utils import timezone
from django.apps import apps
from django.http import HttpResponseBadRequest

# from mw_calc.models import Order
from mw_calc.helpers import isNaN, \
    get_model_name_by_calc_name as get_model_name, \
    get_app_label_by_calc_name as get_app_label, \
    get_calc_session

# from mw_calc.forms import robokassa_form

logger = logging.getLogger('logfile')


def r_start():
    pass


def r_script(script, json_file, filename, with_mean=0, **kwargs):
    calc_name = kwargs.get('calc_name', '')

    args = [
        f'Rscript --vanilla {script} {json_file} {filename} {with_mean} {calc_name}'
    ]

    # logger.debug(
    #     args
    # )

    # print(
    #     args
    # )

    # logger.debug(
        # subprocess.check_output(args, universal_newlines=True, shell=True)
    # )

    return subprocess.check_output(args, universal_newlines=True, shell=True)


def rmd_script(home_dir, script, out_dir, out_file, json_file, html_format=None, desc_file=None, **kwargs):
    calc_string = ''

    if 'calc_name' in kwargs:
        calc_name = kwargs['calc_name']
        calc_string = f',calc_name=\'{calc_name}\''

    args = [
        f'\
            Rscript -e \
            "Sys.setenv(HOME=\'{home_dir}\');\
                rmarkdown::render(\'{script}\',output_dir=\'{out_dir}\',\
                output_file=\'{out_file}\',params=list(json_file=\'{json_file}\',\
                html_format=\'{html_format}\',desc_file=\'{desc_file}\'{calc_string}))\
            "\
        '
    ]


    # print(
    #     args
    # )

    # print(
    #     subprocess.getoutput(args)
    # )

    start_time = time.time()
    subprocess.getoutput(args)
    logger.debug("--- %s seconds --- %s ---" % (time.time() - start_time, calc_string))


    if is_file_exist(out_dir + out_file):
        return True
    else:
        logger.debug(
            '*************************',
            'rmd_script file NOT EXIST',
            subprocess.getoutput(args)
        )
        return False


def send(from_mail, to_mail, msg='', file=False):
    email = EmailMessage(
        'Расчёт на сайте stanly.statpsy.ru',
        msg,
        from_mail,
        to_mail,
    )

    if file:
        email.attach_file(file)

    email.send()


def get_g_recaptcha(token):
    return requests.get(
        s.G_RECAPTCHA_URL,
        params={
            'secret': s.G_RECAPTCHA_KEY,
            'response': token
        }
    ).json()


def get_my_cookie(cookie_name, cookie_string):
    cookie_list = cookie_string.split('; ')
    target_cookie = ''

    for cookie in cookie_list:
        c = cookie.split('=')
        if c[0] == cookie_name:
            target_cookie = c[1]
            break

    return target_cookie


def get_steps(step, calc_name=None):
    return {
        'step':         step,
        'next_step':    step + 1,
        'prev_step':    step - 1,
        'calc_name':    calc_name
    }


def get_context_many_groups(request):
    step = int(get_request_param(request, 'step', 1))  # номер шага
    prev_step = step - 1
    next_step = step + 1
    calc_name = get_request_param(request, 'calc_name')  # название калькулятора
    scales = JSON.loads(get_calc_session(request, calc_name, 'scales'))  # шкалы
    group_quantity = int(get_calc_session(request, calc_name, 'group_quantity')) # количество групп
    group_number = int(get_request_param(request, 'group_number'))  # номер группы
    group_count = int(get_request_param(request, 'group_count'))  # количество человек в группе
    group_name = get_request_param(request, 'group_name') # название группы
    group_next = group_number + 1
    group_prev = group_number - 1 if group_number > 1 else None
    redirect_to = '{0}{1}/steps/{2}/{3}/'.format(s.CALC_INDEX_URL, calc_name, step, group_next)
    back_url = '{0}{1}/steps/{2}/{3}/'.format(s.CALC_INDEX_URL, calc_name, step, group_prev)
    if step == 2:
        if group_number == group_quantity:
            redirect_to = '{0}{1}/steps/{2}/'.format(s.CALC_INDEX_URL, calc_name, next_step)
        elif group_number == 1:
            back_url = '{0}{1}/steps/{2}/'.format(s.CALC_INDEX_URL, calc_name, prev_step)
    elif step == 3:
        back_url = '{0}{1}/steps/{2}/{3}/'.format(s.CALC_INDEX_URL, calc_name, prev_step, group_quantity)

    return {
        'step':         step,
        'next_step':    step + 1,
        'prev_step':    step - 1,
        'calc_name':    calc_name,
        'group_number':    group_number,
        'group_prev':    group_prev,
        'group_next':    group_next,
        'group_quantity':    group_quantity,
        'group_name':    group_name,
        'group_count':    group_count,
        'group_count_range': range(1, group_count + 1),
        'back_url':    back_url,
        'redirect_to':    redirect_to,
        'scales':    scales,

    }


def get_json_out_dir(calc_name):
    return os.path.join(s.BASE_DIR, 'tmp/', (calc_name + '/'), s.JSON_OUT_DIR)


def get_html_out_dir(calc_name):
    return os.path.join(s.BASE_DIR, 'tmp/', (calc_name + '/'), s.HTML_OUT_DIR)


def get_xlsx_out_dir(calc_name):
    return os.path.join(s.BASE_DIR, 'tmp/', (calc_name + '/'), s.XLSX_OUT_DIR)


def get_docx_out_dir(calc_name):
    return os.path.join(s.BASE_DIR, 'tmp/', (calc_name + '/'), s.DOCX_OUT_DIR)


def get_script_dir(calc_name):
    return os.path.join(s.BASE_DIR, s.SCRIPT_DIR, (calc_name + '/'))


def is_file_exist(path):
    return os.path.isfile(path)


def get_html_file(request, html_format, calc_name):
    HTML_OUT_DIR = get_html_out_dir(calc_name)
    SCRIPT_DIR = get_script_dir(calc_name)
    desc_file = get_request_param(request, 'desc_file')

    order_id = request.session['order_id']
    # json_file = request.session['json_file']
    JSON_OUT_DIR = get_json_out_dir(calc_name)
    json_file = os.path.join(JSON_OUT_DIR, (order_id + '.json'))
    html_file = calc_name + '_' + html_format + '_' + order_id + '.html'
    script = os.path.join(SCRIPT_DIR, s.HTML_SCRIPT)

    if 'file' in request.FILES:
        desc_file = request.FILES['file']

    # remove old before creation
    if is_file_exist(HTML_OUT_DIR + html_file):
        os.remove(HTML_OUT_DIR + html_file)

    result = rmd_script(s.HOME_DIR, script, HTML_OUT_DIR, html_file,
               json_file, html_format, desc_file)

    if result:
        return html_file
    else:
        logger.debug(
            'get_html_file',
            html_file,
            json_file
        )
        return False

def is_paid(request, calc_name):
    Order = apps.get_model(app_label='mw_calc', model_name='Order')

    paid_order = Order.objects.filter(
        user=request.user,
        calc_name=calc_name,
        status='paid',
        expire__gt=timezone.now()
    ).order_by('date').first()

    if not paid_order:
        paid_order = Order.objects.filter(
            user=request.user,
            calc_name=calc_name,
            status='paid',
            expire_count__gt=0
        ).order_by('date').first()

    if paid_order:
        return True
    else:
        return False


def expire_count_decrement(request, calc_name):
    Order = apps.get_model(app_label='mw_calc', model_name='Order')
    paid_order = Order.objects.filter(
        user=request.user,
        calc_name=calc_name,
        status='paid',
        expire_count__gt=0
    ).order_by('date').first()

    if paid_order:
        paid_order.expire_count = paid_order.expire_count - 1
        paid_order.save()
    else:
        logger.debug(
            "order has not 'expire_count'"
        )


def get_request_param(request, param, default=None):
    return request.POST.get(param) or request.GET.get(param, default)


def handle_scales_file(file):
    scales = pd.read_excel(file, header=None, usecols=[0], dtype=str)
    scales = scales.fillna(0)
    scales = scales.to_numpy()
    res = list()

    i = 0
    for scale in scales:
        if not isNaN(scale[0]):
            res.append(scale[0])

        i += 1

    return res


def handle_group_file(file):
    data = pd.read_excel(file, header=0, dtype=str)
    data = data.fillna(0)
    length = len(data.index)
    index = pd.Index(list(range(1, length + 1)))
    data = data.set_index(index)
    data = data.to_dict()

    return data


def create_xlsx(request):
    calc_name = get_request_param(request, 'calc_name')
    order_id = get_request_param(request, 'order_id')
    style = get_request_param(request, 'style', 'short')

    if not order_id:
        order_id = request.session['order_id']

    XLSX_OUT_DIR = get_xlsx_out_dir(calc_name)
    SCRIPT_DIR = get_script_dir(calc_name)
    XLSX_SCRIPT = s.XLSX_SCRIPT
    script_file = os.path.join(SCRIPT_DIR, XLSX_SCRIPT)

    JSON_OUT_DIR = get_json_out_dir(calc_name)
    json_file = os.path.join(JSON_OUT_DIR, (order_id + '.json'))

    if not is_file_exist(json_file):
        return HttpResponseBadRequest('no json file')

    xlsx_file = os.path.join(XLSX_OUT_DIR, (style + '_' + order_id + '.xlsx'))
    r_script(script_file, json_file, xlsx_file, style)

    return xlsx_file


def create_docx(request):
    calc_name = get_request_param(request, 'calc_name')
    order_id = get_request_param(request, 'order_id')
    desc_file = get_request_param(request, 'desc_file')

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
    SCRIPT_DIR = get_script_dir(calc_name)
    docx_file = os.path.join(DOCX_OUT_DIR, filename)
    script = os.path.join(SCRIPT_DIR, s.DOCX_SCRIPT)
    rmd_script(s.HOME_DIR, script, DOCX_OUT_DIR,
               docx_file, json_file, 'docx', desc_file)

    return docx_file


# def get_calc_session(request, calc_name):
#     if calc_name in request.session:
#         res = request.session[calc_name]
#     else:
#         res = None
#     return res

# def set_calc_session(request, calc_name, data=None):
#     request.session[calc_name] = data

# def get_order_param(request, calc_name, param, default=None):
#     paid_order = Order.objects.filter(
#         user__exact=request.user,
#         calc_name__exact=calc_name,
#         try_it__gt=0
#     ).first()

#     res = Order.objects.get(name=param)

#     return res


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=100):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(s.MEDIA_ROOT, name))
        return name
