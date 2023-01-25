from django.db.models.signals import pre_save, post_save

from django.dispatch import receiver

from .helper import serialize_check_in
from .models import CheckIn, validate_same_day, validate_member_of_team
from ..analytics.tasks import load_check_in


@receiver(pre_save, sender=CheckIn)
def validate_daily_check_in(signal, sender, instance, **kwargs):
    validate_same_day(instance.user)
    validate_member_of_team(instance.user)


@receiver(post_save, sender=CheckIn)
def send_task(signal, sender, instance, **kwargs):
    load_check_in(serialize_check_in(instance))
