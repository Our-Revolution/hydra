from django.contrib import admin
from .models import Slack


@admin.register(Slack)
class SlackAdmin(admin.ModelAdmin):
    pass