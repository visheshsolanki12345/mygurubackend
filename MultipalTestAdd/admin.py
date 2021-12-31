from django.contrib import admin
from .models import (
    NewClass, PaymentHistory, ShowGrade, Section, Interpretation,
    ImageOptionsTest, OneOptionsTest,
    OptionsTest, AddTest, TestBackupOneQuizeCorrect, TestCategory, Title, SelectNumber, ThreeOptionsTest, FiveOptionsTest,
    Reports, InterpretationGrade, Career, ResultTitle, TestBackupOneImageQuizeCorrect, TestBackupMultipalQuize,
    TestBackupFiveQuize, TestBackupThreeQuize
    )
# Register your models here.

@admin.register(NewClass)
class NewClassModelAdmin(admin.ModelAdmin):
    list_display = ['id','newClass']

@admin.register(Career)
class CareerModelAdmin(admin.ModelAdmin):
    list_display = ['newCareer']


@admin.register(Section)
class SectionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'section']

@admin.register(InterpretationGrade)
class InterpretationGradeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'grade']

@admin.register(ShowGrade)
class ShowGradeModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'section', 'selectGrade', 'score', 'the_json']


@admin.register(Interpretation)
class InterpretationModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'section', 'title','grade', 'selectGrade', 'point', 'the_json', 'the_title']


@admin.register(SelectNumber)
class SelectNumberModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'a', 'b', 'c', 'd', 'e', 'rightAns']


@admin.register(Title)
class TitleModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'description', 'duration', 'price']


@admin.register(ImageOptionsTest)
class ImageOptionsTestModelAdmin(admin.ModelAdmin):
    list_display = ['section', 'question', 'questionText', 'a','aText', 'b','bText', 'c', 'cText', 'd', 'dText', 'rightAns']


@admin.register(OneOptionsTest)
class OneOptionsTestModelAdmin(admin.ModelAdmin):
    list_display = ['section', 'question', 'questionImage', 'a', 'b', 'c', 'd', 'rightAns']


@admin.register(OptionsTest)
class OptionsTestModelAdmin(admin.ModelAdmin):
    list_display = ['career', 'section', 'question', 'a', 'b', 'c', 'd', 'e']


@admin.register(ThreeOptionsTest)
class ThreeOptionsTestModelAdmin(admin.ModelAdmin):
    list_display = ['section', 'question', 'a', 'b', 'c']

@admin.register(FiveOptionsTest)
class FiveOptionsTestModelAdmin(admin.ModelAdmin):
    list_display = ['section', 'question', 'a', 'b', 'c', 'd', 'e']


@admin.register(TestCategory)
class TestCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'selectTest']


@admin.register(ResultTitle)
class ResultTitleModelAdmin(admin.ModelAdmin):
    list_display = ['typeOfTest', 'className', 'mainHeading', 'title', 'discription', 'point', 'the_json']


@admin.register(AddTest)
class AddTestModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'typeOfTest', 'title', 'selectNumber', 'resultTitle', 'createAt']


@admin.register(Reports)
class ReportsModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'Class','carrer', 'section', 'question', 'interpretatio', 'grade', 'totalCount', 'CreateAt', 'industry_Grade', 'typeOftest', 'totalNoQu']

@admin.register(PaymentHistory)
class PaymentHistoryModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'typeOfTest', 'Class', 'ORDER_ID', 'TXN_AMOUNT', 'email', 'status', 'gateway', 'bankname', 'TXNID', 'TXNDATE', 'paymentCount', 'CURRENCY', 'PAYMENTMODE', 'MID', 'RESPCODE']

# @admin.register(TestBackupOneQuizeCorrect)
# class TestBackupOneQuizeCorrectModelAdmin(admin.ModelAdmin):
#     list_display = ['user', 'typeOfTest', 'className', 'oneQuizeCorrect', 'testDiscription', 'userClickObj', 'createAt']

# @admin.register(TestBackupOneImageQuizeCorrect)
# class TestBackupOneImageQuizeCorrectModelAdmin(admin.ModelAdmin):
#     list_display = ['user', 'typeOfTest', 'className', 'imageOneQuizeCorrect', 'testDiscription', 'userClickObj', 'createAt']


# @admin.register(TestBackupMultipalQuize)
# class TestBackupMultipalQuizeModelAdmin(admin.ModelAdmin):
#     list_display = ['user', 'typeOfTest', 'className', 'multipalQuize', 'testDiscription', 'userClickObj', 'createAt']


# @admin.register(TestBackupFiveQuize)
# class TestBackupFiveQuizeModelAdmin(admin.ModelAdmin):
#     list_display = ['user', 'typeOfTest', 'className', 'fiveQuize', 'testDiscription', 'userClickObj', 'createAt']


# @admin.register(TestBackupThreeQuize)
# class TestBackupThreeQuizeModelAdmin(admin.ModelAdmin):
#     list_display = ['user', 'typeOfTest', 'className', 'threeQuize', 'testDiscription', 'userClickObj', 'createAt']


