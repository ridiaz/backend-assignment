from django.apps import AppConfig


class DailyConfig(AppConfig):
    name = 'happiness.daily'

    def ready(self):
        from .signals import validate_daily_check_in, send_task
