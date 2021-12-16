from django.contrib import admin
from .models import  DefinedGrate, DefineClasses, IndustryCategory, Questions, Reports_9th, Test, ShowGrade, Interpretation_9th, GeneralInformation_9th
# Register your models here.

@admin.register(Test)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'duration', 'date','amount', 'testName','grade']


@admin.register(DefinedGrate)
class DefinedTestGrateModelAdmin(admin.ModelAdmin):
    list_display = ['id','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'P_11','P_12' ,'P_13','P_14', 'P_15' , 'toFromPair', 'grade']

@admin.register(DefineClasses)
class GradeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'Class','testInstruction']

@admin.register(IndustryCategory)
class IndustryCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id','industry_Id', 'industry']


@admin.register(Questions)
class QuestionManagementModelAdmin(admin.ModelAdmin):
    list_display = ['id','grade' , 'industry', 'question', ]



@admin.register(Reports_9th)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'industry', 'totalCount', 'grade', 'CreateAt', 'industry_Grade']


@admin.register(ShowGrade)
class ShowGradeModelAdmin(admin.ModelAdmin):
    list_display = ['id','score' , 'grade' ]


@admin.register(Interpretation_9th)
class Interpretation_9thModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'grade', 'interpretationTitle', 'YouCanDoPoint_1', 'YouCanDoPoint_2', 'YouCanDoPoint_3', 'YouCanDoPoint_4', 'YouCanDoPoint_5']


@admin.register(GeneralInformation_9th)
class GeneralInformation_9thModelAdmin(admin.ModelAdmin):
    list_display = ['id','TitleImportance'  ]