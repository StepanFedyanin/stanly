import logging

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
# from .signals import add_new_user
from django.apps import apps
from django.contrib.auth.models import User
from django.conf import settings as s

from allauth.account.signals import user_signed_up, user_logged_in
from allauth.account.models import EmailAddress

# from planfix.models import PlanfixModel
# from planfix.classes import PlanfixError
# from planfix.api import PlanFix

from .helpers import random_promo

logger = logging.getLogger('logfile')
logger_planfix = logging.getLogger('planfix')

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Promo(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name="user"
    )
    active = models.BooleanField('Active?', default=True)
    private = models.BooleanField('Private?', default=False)
    discount = IntegerRangeField(
        verbose_name='Percent %',
        min_value=0,
        max_value=100,
        default=10
    )
    expire = models.DateTimeField(default=timezone.now)
    # user_receiver = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     verbose_name='user receiver',
    #     related_name="user_receiver",
    #     blank=True,
    #     null=True
    # )
    # extra_param = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        get_latest_by = 'expire'

    def __str__(self):
        return self.name


# @receiver(user_signed_up)
# def orders_create_on_signed_up(sender, **kwargs):
#     """
#         При регистрации
#         Создать orders по калькуляторам
#     """
#     user = kwargs["sociallogin"].user if "sociallogin" in kwargs else kwargs["user"]
#     order_list = [
#             Order(user=user, calc_name=calc_name, status='')
#                 for calc_name in s.CALC_NAMES
#         ]

#     Order.objects.bulk_create(order_list)


@receiver(user_signed_up)
def promo_create_on_signed_up(sender, **kwargs):
    """
        При регистрации
        Создать promo для пользователя
        # sociallogin = allauth.socialaccount.models.SocialLogin
        # sender = django.contrib.auth.models.User
    """
    user = kwargs["sociallogin"].user if "sociallogin" in kwargs else kwargs["user"]

    Promo.objects.create(
        name=random_promo(),
        user=user,
        active=True,
        private=True,
        expire=timezone.now() + timezone.timedelta(days=365)
    )


@receiver(user_logged_in)
def planfix_create_contact_on_sign_up(sender, **kwargs):
    """
        При авторизации
        Добваить запись, оправить в planfix
    """
    vk = ''
    if "sociallogin" in kwargs:
        user = kwargs["sociallogin"].user
        vk = kwargs["sociallogin"].account
    else:
        user = kwargs["user"]

    obj, created = PlanfixModel.objects.get_or_create(user=user)

    if obj.contact_id is None:
        initial = s.PLANFIX_INITIAL
        mw_chunk = apps.get_model(app_label='mw_calc', model_name='Chunk')
        planfix_password = mw_chunk.objects.get(name='planfix_password').value

        if planfix_password:
            initial["PLANFIX_PASSWORD"] = planfix_password

        try:
            p = PlanFix(**initial)
            p.debug = logger_planfix.debug
            new_contact = {
                "account": initial["account"],
                "template": initial["contacts_template"],
                "name": user.username,
                "email": user.email,
                "regDate": user.date_joined.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
            }

            if vk:
                new_contact["name"] = user.first_name
                new_contact["lastName"] = user.last_name
                new_contact["vk"] = f'https://vk.com/{vk}'
            else:
                new_contact["name"] = user.username

            try:
                contact_id = p.contact_add(**new_contact)
                if contact_id:
                    obj.contact_id = int(contact_id)
                    obj.save()
            except (ValueError, TypeError):
                return None
        except PlanfixError as er:
            logger_planfix.debug(f'Planfix Error: {er.code} - {er.message}')
            logger_planfix.debug(user.username)
            logger_planfix.debug(user.email)
            logger_planfix.debug('')

    if obj.task_id is None:
        initial = s.PLANFIX_INITIAL
        mw_chunk = apps.get_model(app_label='mw_calc', model_name='Chunk')
        planfix_password = mw_chunk.objects.filter(name='planfix_password').first()
        initial["PLANFIX_PASSWORD"] = planfix_password.value

        try:
            p = PlanFix(**initial)
            p.debug = logger_planfix.debug
            new_task = {
                "account": initial["account"],
                "title": f"(stanly.statpsy.ru) {user.username}",
                "importance": "AVERAGE",
                "template": initial["task_template_id"],
                "status": initial["status_id_1"],
                "statusSet": initial["process_id"],
                "project": initial["project_id"],
            }

            try:
                contact_id
            except NameError:
                pfm = PlanfixModel.objects.get(user=user)
                contact_id = pfm.contact_id

            new_task['owner'] = contact_id

            try:
                task_id = p.task_add(**new_task)
                obj.task_id = int(task_id)
                obj.save()
            except (ValueError, TypeError):
                return None
        except PlanfixError as er:
            logger_planfix.debug(f'Planfix Error: {er.code} - {er.message}')
            logger_planfix.debug(user.username)
            logger_planfix.debug(user.email)
            logger_planfix.debug('')
