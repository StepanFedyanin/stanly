from django.http import HttpResponseRedirect
from django.conf import settings as s
import requests
import random
import uuid

from .utils import get_g_recaptcha, get_my_cookie
from .models import Order
from .helpers import del_session_keys


class CalcMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if 'HTTP_COOKIE' in request.META:
            ya_client_id = get_my_cookie(
                '_ym_uid', request.META['HTTP_COOKIE'])

            # if 'ya_client_id' not in request.session or request.session['ya_client_id'] != ya_client_id:
            if 'ya_client_id' not in request.session:
                del_session_keys(request)
                request.session['ya_client_id'] = ya_client_id
                payment_id = random.randint(20000, 200000) * 5 - 1
                request.session['order_id'] = ya_client_id + \
                    '_' + str(payment_id)

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        request.session['price_type'] = self.getRandomPrice()

        return response

    def getRandomPrice(self):
        if random.random() > 0.5:
            return 'price_test'
        else:
            return 'price'
