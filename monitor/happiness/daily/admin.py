from django.contrib import admin

from .models import CheckIn


@admin.register(CheckIn)
class TeamModelAdmin(admin.ModelAdmin):
    list_display = ['responses', 'created', 'user']
