from django.contrib import admin
from .models import  DefinedGrate, DefineClasses, IndustryCategory, Questions, Reports_8th, Test, ShowGrade, GeneralInformation_8th, Interpretation_8th
# Register your models here.

@admin.register(Test)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'duration', 'date','amount', 'testName','grade']


@admin.register(DefinedGrate)
class DefinedTestGrateModelAdmin(admin.ModelAdmin):
    list_display = ['id','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'toFromPair', 'grade']

@admin.register(DefineClasses)
class GradeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'Class','testInstruction']

@admin.register(IndustryCategory)
class IndustryCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id','industry_Id', 'industry']


@admin.register(Questions)
class QuestionManagementModelAdmin(admin.ModelAdmin):
    list_display = ['id','grade' , 'industry', 'question', 'rightAns']



@admin.register(Reports_8th)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'industry', 'totalCount', 'grade', 'CreateAt', 'industry_Grade']


@admin.register(ShowGrade)
class ShowGradeModelAdmin(admin.ModelAdmin):
    list_display = ['id','score' , 'grade' ]

@admin.register(GeneralInformation_8th)
class GeneralInformation_8thModelAdmin(admin.ModelAdmin):
    list_display = ['id','TitleImportance' ]


@admin.register(Interpretation_8th)
class Interpretation_8thModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'grade', 'interpretationTitle', 'YouCanDoPoint_1', 'YouCanDoPoint_2', 'YouCanDoPoint_3', 'YouCanDoPoint_4', 'YouCanDoPoint_5']
