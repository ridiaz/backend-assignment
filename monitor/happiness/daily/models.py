from django.db import models

from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import APIException

from ..team.models import Team


class CheckIn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    responses = models.JSONField(default=list)
    created = models.DateTimeField(auto_now_add=True)


def validate_same_day(user):
    now = timezone.now()
    try:
        latest = CheckIn.objects.filter(user=user).latest('created')
    except CheckIn.DoesNotExist:
        return
    offset_24_hours = latest.created + timedelta(hours=24)
    if now < offset_24_hours:
        raise APIException('Only one check-in is allowed in a same day')


def validate_member_of_team(user):
    if not Team.objects.filter(users__pk=user.id).exists():
        raise APIException('User is not a member of any Team')
