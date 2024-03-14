import os
import json as JSON
from collections.abc import Iterable
# import xlsxwriter

from django.http import HttpResponse, HttpResponseBadRequest
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator

from mw_calc.views import get_xlsx_out_dir, get_script_dir
from mw_calc.utils import *
from mw_calc.helpers import set_calc_session, get_calc_session, get_chunk_value_by_name
# from mw_calc.decorators import check_payment

from django.conf import settings as s

import logging
logger = logging.getLogger('logfile')


def create_xlsx(request):
    calc_name = get_request_param(request, 'calc_name')
    order_id = get_request_param(request, 'order_id')
    style = get_request_param(request, 'style', 'short')

    if not order_id:
        order_id = request.session['order_id']

    XLSX_OUT_DIR = get_xlsx_out_dir(calc_name)
    SCRIPT_DIR = get_script_dir(calc_name)
    XLSX_SCRIPT = s.XLSX_SCRIPT
    script = os.path.join(SCRIPT_DIR, XLSX_SCRIPT)

    JSON_OUT_DIR = get_json_out_dir(calc_name)
    json_file = os.path.join(JSON_OUT_DIR, (order_id + '.json'))

    if not is_file_exist(json_file):
        return HttpResponseBadRequest('no json file')

    xlsx_file = os.path.join(XLSX_OUT_DIR, (style + '_' + order_id + '.xlsx'))
    r_script(script, json_file, xlsx_file, style)

    return xlsx_file


def set_group_data(request):
    if request.method == "POST":
        params = dict(request.POST.items())
        group_number = int(params['group_number'])
        group_count = int(params['group_count'])
        group_name = params['group_name']
        calc_name = params['calc_name']

        group_data = JSON.loads(params['group_data'])
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


def get_file(request):
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
