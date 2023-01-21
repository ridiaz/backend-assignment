from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)


