from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

import logging
logger = logging.getLogger('logfile')
