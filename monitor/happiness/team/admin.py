from django.contrib import admin

from .models import Team

TITLE = 'D1g1t Backend management'

admin.site.site_header = TITLE
admin.site.index_title = TITLE


@admin.register(Team)
class TeamModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created']
