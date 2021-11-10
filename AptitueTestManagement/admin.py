from django.contrib import admin
from .models import TestScheduleManagement
# Register your models here.

@admin.register(TestScheduleManagement)
class IndustryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'duration', 'date','amount', 'testName']