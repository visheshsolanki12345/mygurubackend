from django.contrib import admin
from .models import TestScheduleManagement, QuestionManagement, IndustryCategory, TestResult, DefinedTestGrate, ShowGrade
# Register your models here.

@admin.register(TestScheduleManagement)
class IndustryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'duration', 'date','amount', 'testName','grade']

@admin.register(QuestionManagement)
class QuestionManagementModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'industry', 'question']

@admin.register(IndustryCategory)
class IndustryCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'industry_Id', 'industry']


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'industry', 'totalCount', 'grade', 'CreateAt', 'industry_Grade']

@admin.register(DefinedTestGrate)
class DefinedTestGrateModelAdmin(admin.ModelAdmin):
    list_display = ['id','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'toFromPair', 'grade']

@admin.register(ShowGrade)
class ShowGradeModelAdmin(admin.ModelAdmin):
    list_display = ['id','score' , 'grade' ]
