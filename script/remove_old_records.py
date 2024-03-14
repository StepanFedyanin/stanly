from django.utils import timezone
import datetime
from mw_calc.models import Calculation, Order
from django.contrib.auth.models import User

ago = timezone.now() - datetime.timedelta(days=30*6) # 180 days ago
# Calculation.objects.filter(date__lt=ago).delete()
# Order.objects.filter(date__lt=ago).delete()
# User.robjects.filter(date__lt=ago).delete()
