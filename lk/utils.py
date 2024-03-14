from django.utils import timezone

from .models import Promo


def get_promo_by_user(user):
    try:
        promo = Promo.objects.filter(
            user=user
        )
    except Promo.DoesNotExist:
        promo = None

    return promo
