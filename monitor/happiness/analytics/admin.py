from django.contrib import admin

from .models import DimensionTeam, DimensionDate, DimensionHappinessLevel, FactResponse


@admin.register(DimensionTeam)
class DimensionTeamModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(DimensionDate)
class DimensionDateModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'month', 'day']


@admin.register(DimensionHappinessLevel)
class DimensionHappinessLevelModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'level']


@admin.register(FactResponse)
class FactResponseModelAdmin(admin.ModelAdmin):
    pass
