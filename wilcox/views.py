from django.shortcuts import render
import json as JSON
from django.http import HttpResponse, HttpResponseBadRequest
from mw_calc.helpers import get_calc_session, set_calc_session, get_chunk_value_by_name
from mw_calc.utils import get_request_param

import logging
logger = logging.getLogger('logfile')


def get_group_inputs(request):
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

            group_count_1 = get_calc_session(request, calc_name, 'group_count_1')
            if group_number == 2 and group_count_1 != group_count:
                return HttpResponseBadRequest('count')

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
