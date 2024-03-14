from django.contrib import admin
from django.urls import path, re_path

from .views import *

from mw_calc.views import *

app_name = 'w'

urlpatterns = [
    path('', home_page.as_view(calc_name=app_name)),

    re_path(r'^steps/(?P<step>[0-3]){1}/$',
            steps_no_auth.as_view(calc_name=app_name)),
    re_path(r'^steps/(?P<step>[4]){1}/$',
            steps_auth.as_view(calc_name=app_name)),
    re_path(r'^steps/(?P<step>[5-7]){1}/$',
            steps_payment.as_view(calc_name=app_name)),

    path('send_xlsx/', calc_send_xlsx),
    path('send_xlsx_full/', calc_send_xlsx),
    path('send_docx/', calc_send_docx),

    path('get_group_inputs/', calc_get_group_inputs),
    path('get_file/', calc_get_file),
    path('get_xlsx_template/', calc_get_xlsx_template),

    path('set_scales/', calc_set_scales),
    path('set_group_data/', set_group_data),
    path('set_json/', calc_set_json),

    path('upload_scales/', calc_upload_scales),
    path('upload_group/', calc_upload_group),
]
