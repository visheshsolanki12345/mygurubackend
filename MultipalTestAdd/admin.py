from django.contrib import admin
from .models import (
    NewClass, PaymentHistory, SelectAcademic, ShowGrade, Section, Interpretation,
    ImageOptionsTest, OneOptionsTest,
    OptionsTest, AddTest, TestBackupOneQuizeCorrect, TestCategory, Title, SelectNumber, ThreeOptionsTest, 
    FiveOptionsTest, Reports, InterpretationGrade, Career, ResultTitle, TestBackupOneImageQuizeCorrect, 
    TestBackupMultipalQuize,TestBackupFiveQuize, TestBackupThreeQuize, AddClassSection, SectionInterest
    ,CarrerDescription
    )
# Register your models here.
from django.contrib.admin import AdminSite, sites


# @admin.register(SelectAcademic)
# class SelectAcademicModelAdmin(admin.ModelAdmin): 
#     list_display = ['id', 'classOrCollage']

@admin.register(NewClass)
class NewClassModelAdmin(admin.ModelAdmin):
    list_display = ['newClass', 'classOrCollage']

# @admin.register(Career)
# class CareerModelAdmin(admin.ModelAdmin):
#     list_display = ['newCareer']

@admin.register(AddClassSection)
class AddClassSectionModelAdmin(admin.ModelAdmin):
    list_display = ['classSection']
    search_fields = ['classSection']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(SectionInterest)
class SectionInterestAdmin(admin.ModelAdmin):
    list_display = ['sectionInterest']

@admin.register(Section)
class SectionModelAdmin(admin.ModelAdmin):
    list_display = [ 'section', 'sectionInterest', 'number', 'duration']
    search_fields = ['section']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(ImageOptionsTest)
class ImageOptionsTestModelAdmin(admin.ModelAdmin):
    list_display = [
        'section', 'questionText', 'aText', 'bText', 'cText', 'dText', 'eText',
        'question', 'a', 'b', 'c', 'd', 'e', 'rightAns'
        ]

    search_fields = ['section__section', 'question']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    # list_display = ['section', 'question', 'questionText', 'a','aText', 'b','bText', 'c', 'cText', 'd', 'dText', 'rightAns']


@admin.register(OneOptionsTest)
class OneOptionsTestModelAdmin(admin.ModelAdmin):
    list_display = ['section', 'question', 'questionImage', 'a', 'b', 'c', 'd', 'rightAns']
    search_fields = ['section__section', 'question']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(OptionsTest)
class OptionsTestModelAdmin(admin.ModelAdmin):
    list_display = ['career', 'section', 'question', 'a', 'b', 'c', 'd', 'e']
    search_fields = ['section__section', 'question']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(ThreeOptionsTest)
class ThreeOptionsTestModelAdmin(admin.ModelAdmin):
    list_display = ('section', 'question', 'a', 'b', 'c')
    search_fields = ['section__section', 'question']
    list_per_page = 10 
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(FiveOptionsTest)
class FiveOptionsTestModelAdmin(admin.ModelAdmin):
    list_display = ['section', 'question', 'a', 'b', 'c', 'd', 'e']
    search_fields = ['section__section', 'question']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# @admin.register(TestCategory)
# class TestCategoryModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'selectTest']


@admin.register(InterpretationGrade)
class InterpretationGradeModelAdmin(admin.ModelAdmin):
    list_display = ['grade']


@admin.register(ShowGrade)
class ShowGradeModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'classSection', 'section', 'the_json']
    search_fields = [
        'className__newClass', 'classSection__classSection', 
        'section__section'
        ]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(Interpretation)
class InterpretationModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'classSection', 'section', 'title','grade', 'selectGrade', 'point', 'the_json', 'the_title']
    search_fields = [
        'className__newClass', 'classSection__classSection', 
        'section__section'
        ]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(SelectNumber)
class SelectNumberModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'classSection', 'a', 'b', 'c', 'd', 'e', 'rightAns']
    search_fields = [
        'className__newClass', 'classSection__classSection', 
        ]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(Title)
class TitleModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'classSection',  'duration', 'price']
    search_fields = [
        'className__newClass', 'classSection__classSection', 
        ]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(ResultTitle)
class ResultTitleModelAdmin(admin.ModelAdmin):
    # list_display = ['typeOfTest', 'className', 'classSection', 'mainHeading', 'title', 'discription', 'point', 'pointDiscription', 'the_json']
    list_display = ['typeOfTest', 'className', 'classSection', 'mainHeading', 'title']
    search_fields = [
        'className__newClass', 'classSection__classSection', 
        'typeOfTest__selectTest'
        ]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(AddTest)
class AddTestModelAdmin(admin.ModelAdmin):
    list_display = ['className', 'classSection', 'typeOfTest', 'title', 'selectNumber', 'resultTitle', 'createAt']
    search_fields = [
        'className__newClass', 'classSection__classSection', 
        'typeOfTest__selectTest'
        ]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(Reports)
class ReportsModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'Class', 'classSection', 'sectionInterest', 'carrer', 'section', 'interpretatio', 'grade', 'totalCount', 'typeOftest', 'totalNoQu']

@admin.register(PaymentHistory)
class PaymentHistoryModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'typeOfTest', 'classSection', 'Class', 'ORDER_ID', 'TXN_AMOUNT', 'email', 'status', 'gateway', 'bankname', 'TXNID', 'TXNDATE', 'paymentCount', 'CURRENCY', 'PAYMENTMODE', 'MID', 'RESPCODE']

# @admin.register(TestBackupOneQuizeCorrect)
# class TestBackupOneQuizeCorrectModelAdmin(admin.ModelAdmin):
#     list_display = ['user', 'typeOfTest', 'className', 'classSection', 'oneQuizeCorrect', 'testDiscription', 'userClickObj', 'lastTime', 'number']


@admin.register(TestBackupOneImageQuizeCorrect)
class TestBackupOneImageQuizeCorrectModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'typeOfTest', 'className', 'classSection', 'imageOneQuizeCorrect', 'testDiscription', 'userClickObj', 'lastTime', 'number']


# @admin.register(TestBackupMultipalQuize)
# class TestBackupMultipalQuizeModelAdmin(admin.ModelAdmin):
#     list_display = ['user', 'typeOfTest', 'className', 'classSection', 'multipalQuize', 'testDiscription', 'userClickObj', 'lastTime', 'number']


# @admin.register(TestBackupFiveQuize)
# class TestBackupFiveQuizeModelAdmin(admin.ModelAdmin):
#     list_display = ['user', 'typeOfTest', 'className', 'classSection', 'fiveQuize', 'testDiscription', 'userClickObj', 'lastTime', 'number']


# @admin.register(TestBackupThreeQuize)
# class TestBackupThreeQuizeModelAdmin(admin.ModelAdmin):
#     list_display = ['user', 'typeOfTest', 'className', 'classSection', 'threeQuize', 'testDiscription', 'userClickObj', 'lastTime', 'number']


# @admin.register(CarrerDescription)
# class CarrerDescriptionAdmin(admin.ModelAdmin):
#     list_display = ['carrer', 'section', 'description']



def get_app_list(self, request):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    # Retrieve the original list
    app_dict = self._build_app_dict(request)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the models customably within each app.
    for app in app_list:
        if app['app_label'] == 'auth':
            ordering = {
                'Users': 1,
                'Groups': 2
            }
            app['models'].sort(key=lambda x: ordering[x['name']])

    return app_list

admin.AdminSite.get_app_list = get_app_list
