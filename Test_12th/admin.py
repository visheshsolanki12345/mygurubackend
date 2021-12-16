from django.contrib import admin
from .models import (
    DefinedGrate, DefineClasses, IndustryCategory, Questions, Reports_12th, Test, ShowGrade, GeneralInformation_12th, Interpretation_12th
)
                            
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
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'industry', 'question']



@admin.register(Reports_12th)
class Reports_10thAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'interpretatio', 'industry', 'totalCount', 'grade', 'CreateAt', 'industry_Grade']


@admin.register(GeneralInformation_12th)
class GeneralInformation_10thModelAdmin(admin.ModelAdmin):
    list_display = ['id','TitleImportance' , 'VerbalAbility', 'NumericalAbility', 'AbstractReasoning', 'LogicalReasoningAbility', 'MechanicalAbility']


@admin.register(Interpretation_12th)
class Interpretation_10thModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'grade', 'interpretationTitle', 'YouCanDoPoint_1', 'YouCanDoPoint_2', 'YouCanDoPoint_3', 'YouCanDoPoint_4', 'YouCanDoPoint_5']


@admin.register(ShowGrade)
class ShowGradeModelAdmin(admin.ModelAdmin):
    list_display = ['id','score' , 'grade' ]