from django.contrib import admin
from django.urls import path, re_path

from .views import *
from mw_calc.views import *

app_name = 'anova'

urlpatterns = [
    path('', calc_home_page.as_view(calc_name=app_name), name='home'),

    re_path(r'^steps/(?P<step>1)/$', Scales.as_view(calc_name=app_name)),
    re_path(r'^steps/(?P<step>2)/(?P<group>\d+)/$',
            Groups.as_view(calc_name=app_name)),
    re_path(r'^steps/(?P<step>3)/$', Prepare.as_view(calc_name=app_name)),
    re_path(r'^steps/(?P<step>4)/$', Auth.as_view(calc_name=app_name)),
    re_path(r'^steps/(?P<step>[5-7]){1}/$', Pay.as_view(calc_name=app_name)),

    path('send_xlsx/', calc_send_xlsx),
    path('send_xlsx_full/', calc_send_xlsx),
    path('send_docx/', calc_send_docx),

    path('get_group_inputs/', GetGroupInputs),
    path('get_file/', GetFile),
    path('get_xlsx_template/', calc_get_xlsx_template),

    path('set_scales/', SetScales),
    path('set_group_data/', calc_set_group_data),
    path('set_json/', calc_set_json),

    path('upload_scales/', calc_upload_scales),
    path('upload_group/', calc_upload_group),
]
