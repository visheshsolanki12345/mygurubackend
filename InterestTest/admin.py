from django.contrib import admin
from .models import (
    Section, InterpretationGrade, ShowGrade,
    Interpretation, SelectNumber, AddQuestion
)
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'typeOfSection', 'section']

@admin.register(InterpretationGrade)
class InterpretationGradeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'grade']

@admin.register(ShowGrade)
class ShowGradeModelAdmin(admin.ModelAdmin):
    list_display = ['selectGrade', 'section', 'score', 'the_json']


@admin.register(Interpretation)
class InterpretationModelAdmin(admin.ModelAdmin):
    list_display = ['section', 'title','grade', 'selectGrade', 'point', 'the_json', 'the_title']


@admin.register(SelectNumber)
class SelectNumberModelAdmin(admin.ModelAdmin):
    list_display = ['section', 'numberEachQuestion']

@admin.register(AddQuestion)
class AddQuestionAdmin(admin.ModelAdmin):
    list_display = ['section', 'question', 'questionText', 'a','aText', 'b','bText', 'c', 'cText', 'd', 'dText', 'rightAns']


