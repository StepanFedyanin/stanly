import logging

from datetime import datetime, timedelta
from django.conf import settings as s
from django.db import models
from django.apps import apps
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce import HTMLField
from robokassa.signals import result_received

from planfix.models import PlanfixModel
from planfix.classes import PlanfixError
from planfix.api import PlanFix

from lk.models import Promo
# from .helpers import get_chunk_value_by_name

logger = logging.getLogger('logfile')
logger_planfix = logging.getLogger('planfix')


CALC_NAMES = (
    ("CT", "compare_two"),
    ("CRS", "correlation_spearman"),
    ("CRP", "correlation_pearson"),
    ("CRK", "correlation_kendall"),
    ("FA", "factor_analytic"),
    ("KR", "kruskal"),
    ("MW", "mann_whitney"),
    ("SI", "student_ind"),
    ("WC", "wilcox"),
    ("W", "w"),
    ("Z", "z"),
    ("AN", "anova"),
)


class Order(models.Model):
    calc_name = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    promo = models.ForeignKey(
        Promo,
        on_delete=models.SET_NULL,
        verbose_name='Promo',
        null=True,
        blank=True
    )
    expire = models.DateTimeField(default=timezone.now)
    expire_count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    extra_param = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        get_latest_by = 'date'


class BaseChunk(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Title",
        blank=True
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Variable"
    )

    value = models.TextField(
        verbose_name="Value",
        blank=True
    )

    html = HTMLField(
        verbose_name="HTML value",
        blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Calc(models.Model):
    name = models.CharField(
        max_length=8,
        choices=CALC_NAMES,
        unique=True
    )
    active = models.BooleanField('Active?')

    class Meta:
        verbose_name = "Calc"
        verbose_name_plural = "Calcs"


class Calculation(models.Model):
    # TODO:
    # поле date заменить на поле last_update
    order_id = models.CharField(max_length=255)
    calc_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
    )

    class Meta:
        get_latest_by = 'date'
        verbose_name = "Calculation"
        verbose_name_plural = "Calculations"

    def save(self, *args, **kwargs):
        planfix_model = PlanfixModel.objects.get(user=self.user)
        task_id = planfix_model.task_id

        if task_id is not None:

            planfix_calc_id = s.PLANFIX_CALCS[self.calc_name]

            initial = s.PLANFIX_INITIAL
            planfix_password = Chunk.objects.get(name='planfix_password').value
            initial["PLANFIX_PASSWORD"] = planfix_password

            task_get = {
                "id": str(task_id),
                "custom_data_id": initial["custom_data_id"]
            }

            try:
                p = PlanFix(**initial)
                p.debug = logger_planfix.debug
                calc_list = p.task_get_field_value(**task_get)

                if not isinstance(calc_list, PlanfixError):
                    if planfix_calc_id not in calc_list:
                        calc_list.append(planfix_calc_id)
                        task_update = {
                            "taskId": str(task_id),
                            "custom_data": [
                              {
                                'id': initial["custom_data_id"],
                                'value': str(calc_list)
                              }
                            ],
                        }
                        p.task_update_v2(**task_update)
                else:
                    er = calc_list
                    logger_planfix.debug(
                        f'Planfix Error: {er.code} - {er.message}',
                        'initial',
                        initial
                    )
            except PlanfixError as er:
                logger_planfix.debug(
                    f'Planfix Error: {er.code} - {er.message}',
                    'initial',
                    initial
                )

        super(Calculation, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username + ' / ' + self.calc_name


class Chunk(BaseChunk):
    pass


@receiver(result_received)
def payment_received(sender, **kwargs):
    """
        При оплате заказа № InvId
    """

    extra = kwargs['extra']
    invid = kwargs['InvId']

    price_type = extra['price_type']
    full_price = extra['full_price']

    order = Order.objects.get(pk=invid)
    user = order.user

    if price_type == 'price_all':
        order_list = list()

        for calc_name in s.CALC_NAMES:
            calc_order = Order.objects.get_or_create(
                user=user,
                calc_name=calc_name,
                status='',
                price=full_price
            )[0]

            calc_order.status = 'paid'
            calc_order.price = full_price
            calc_order.expire = timezone.now() + timedelta(days=1)

            order_list.append(calc_order)

        Order.objects.bulk_update(
            order_list,
            ['status', 'expire', 'expire_count', 'price']
        )

    order.status = 'paid'

    if price_type == 'price_once':
        order.expire_count = order.expire_count + 1
    else:
        order.expire = timezone.now() + timedelta(days=1)

    order.save()

    planfix_model = PlanfixModel.objects.get(user=user)
    task_id = planfix_model.task_id

    if task_id is not None:
        initial = s.PLANFIX_INITIAL
        mw_chunk = apps.get_model(app_label='mw_calc', model_name='Chunk')
        planfix_password = mw_chunk.objects.get(name='planfix_password').value
        initial["PLANFIX_PASSWORD"] = planfix_password

        new_action = {
            'analiticId': initial['analitic_id'],
            'description': '(stanly.statpsy.ru) Добавление аналитики',
            # 'taskGeneral': task_id,
            'taskId': str(task_id),
            'taskNewStatus': initial['status_id_2'],
            # 'userIdList': initial[''],
            # 'isHidden': initial[''],
            # 'ownerId': initial[''],
            # 'dateTime': initial[''],
            'analitic_data': [
                {'field_id': '2040',
                 'value': str(full_price)
                },
                {'field_id': '2042',
                 'value': datetime.now().strftime("%d-%m-%Y")
                },
                {'field_id': '2044',
                 'value': f'(stanly.statpsy.ru) Оплата по калькулятору {order.calc_name} ({price_type})'
                },
            ]
        }


        try:
            p = PlanFix(**initial)
            p.debug = logger_planfix.debug

            action_id = p.action_add(**new_action)
            task_update = {
                "taskId": str(task_id),
                "custom_data": [
                  {
                    'id': initial["custom_data_id_order"],
                    'value': str(invid)
                  }
                ],
            }

            p.task_update_v2(**task_update)

        except PlanfixModel.DoesNotExist:
            logger_planfix.debug(
                'PlanfixModel.DoesNotExist',
                PlanfixModel.DoesNotExist
            )
