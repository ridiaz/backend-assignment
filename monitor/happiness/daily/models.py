from django.db import models

from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import APIException


class CheckIn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    responses = models.JSONField(default=list)
    created = models.DateTimeField(auto_now_add=True)


def verify_same_day(user):
    now = timezone.now()
    try:
        latest = CheckIn.objects.filter(user=user).latest('created')
    except CheckIn.DoesNotExist:
        return
    offset_24_hours = latest.created + timedelta(hours=24)
    if now < offset_24_hours:
        raise APIException('Only one check-in is allowed in a same day')
