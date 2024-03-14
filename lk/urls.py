from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from mw_calc import settings
from .views import *

app_name = 'lk'

urlpatterns = [
    path('clear/', clear),
    path('profile/', profile),
    path('promo/', promo),
    path('history/', history_list),
    path('history/<calc_name>/', history),
    path('email/', ProfileEmailView.as_view()),
    path('confirm-email/', ProfileEmailVerificationSentView.as_view()),
    path('login/', ProfileLoginView.as_view()),
    path('signup/', ProfileSignupView.as_view()),
    path('password/reset/', ProfilePasswordResetView.as_view()),
    path('apply_promo/', apply_promo),
    path('create_promo/', create_promo),
    path('delete_promo/', delete_promo),

    path('signup_ajax/', AjaxSignupView.as_view()),
    path('login_ajax/', AjaxLoginView.as_view()),
    path('reset_password_ajax/', AjaxPasswordResetView.as_view()),
    path('reset_password_done_ajax/', AjaxPasswordResetDoneView.as_view()),
    path('verification_sent_ajax/', AjaxEmailVerificationSentView.as_view()),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        ProfilePasswordResetFromKeyView.as_view()),
    # path('password/reset/key/done/', AjaxEmailVerificationSentView.as_view()),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
