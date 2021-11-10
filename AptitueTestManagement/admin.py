from django.contrib import admin
from .models import TestScheduleManagement, QuestionManagement
# Register your models here.

@admin.register(TestScheduleManagement)
class IndustryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'duration', 'date','amount', 'testName']

@admin.register(QuestionManagement)
class QuestionManagementModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'industry', 'question']