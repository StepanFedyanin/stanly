from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from . import settings as s
from .views import g_captcha

from mw_calc.views import *

app_name = 'mw_calc'


class tilda(TemplateView):
    template_name = "tilda/index.html"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tilda.as_view()),
    path('dogovor', dogovor.as_view()),
    path('tilda_get_pages/', tilda_get_pages),
    path('all/', index.as_view()),

    path('all/ajax/achievement_close/', achievement_close),
    path('all/ajax/get_video/', get_video),
    path('all/ajax/session_clear/', session_clear),
    path('all/ajax/get_sample/', get_sample),
    path('all/ajax/get_full_example/', get_full_example),
    path('all/ajax/get_payment_methods/', get_payment_methods_ajax),
    path('all/ajax/get_payment_form/', get_payment_form_ajax),

    path('all/mann_whitney/', include('mann_whitney.urls'), name='mann_whitney'),
    path('all/wilcox/', include('wilcox.urls'), name='wilcox'),
    path('all/compare_two/', include('compare_two.urls'), name='compare_two'),
    path('all/student_ind/', include('student_ind.urls'), name='student_ind'),
    path('all/kruskal/', include('kruskal.urls'), name='kruskal'),
    path('all/w/', include('w.urls'), name='w'),
    path('all/z/', include('z.urls'), name='z'),
    path('all/desc/', include('desc.urls'), name='desc'),
    path(
        'all/correlation_spearman/',
        include('correlation.urls', namespace='correlation-spearman'),
        {'correlation_name': 'correlation_spearman'}
    ),
    path(
        'all/correlation_pearson/',
        include('correlation.urls', namespace='correlation-pearson'),
        {'correlation_name': 'correlation_pearson'}
    ),
    path(
        'all/correlation_kendall/',
        include('correlation.urls', namespace='correlation-kendall'),
        {'correlation_name': 'correlation_kendall'}
    ),
    path('all/factor_analytic/', include('factor_analytic.urls'), name='factor_analytic'),
    path('all/anova/', include('anova.urls'), name='anova'),

    path('all/sample/<calc_name>/', sample),

    path('all/robokassa/', include('robokassa.urls')),

    path('all/accounts/', include('lk.urls')),
    path('all/accounts/', include('allauth.urls')),
    path('all/g_captcha/', g_captcha),
    re_path(r'^tinymce/', include('tinymce.urls')),

    re_path(r'^robots.txt$', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),
]

if s.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
