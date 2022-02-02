from django.contrib import admin
from .models import CarrerType, Carrer, CarrerPage, StudentFeaturedArticle, EditorApproveArticle, Counsellor, CounsellorSlot, BookUserSlot


# Register your models here.
@admin.register(CarrerType)
class CarrerTypeAdmin(admin.ModelAdmin):
    list_display = ['typeOfCarrer']

@admin.register(Carrer)
class CarrerAdmin(admin.ModelAdmin):
    list_display = ['carrerType', 'carrer']

@admin.register(CarrerPage)
class CarrerPageAdmin(admin.ModelAdmin):
    list_display = ['carrer', 'heading', 'bannerImage', 'description']
    
@admin.register(StudentFeaturedArticle)
class StudentFeaturedArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'carrer', 'heading', 'description', 'bannerImage', 'articleApprove', 'createAt']

@admin.register(EditorApproveArticle)
class EditorApproveArticleAdmin(admin.ModelAdmin):
    list_display = ['user', 'studentArticle', 'paymentChoices', 'articleApprove', 'ammount', 'createAt']

@admin.register(Counsellor)
class CounsellorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'carrer', 'title', 'qualification', 'mobile', 'experience', 'college', 'designation', 'address', 'pincode', 'area', 'aboutUs', 'language', 'price', 'dateOfBirth', 'gender', 'createAt']


@admin.register(CounsellorSlot)
class CounsellorSlotAdmin(admin.ModelAdmin):
    list_display = ['counsellor', 'date', 'timeFrom', 'timeTo', 'isBook', 'bookedUser']


@admin.register(BookUserSlot)
class BookUserSlotAdmin(admin.ModelAdmin):
    list_display = ['user', 'counsellorSlot']

