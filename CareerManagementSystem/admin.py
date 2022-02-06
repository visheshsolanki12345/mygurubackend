from django.contrib import admin
from .models import (
    CarrerType, Carrer, CarrerPage, StudentFeaturedArticle, 
    EditorApproveArticle, Counsellor, CounsellorSlot, BookUserSlot,
    ArticleRating, ArticleNoView, CounsellorRating, CounsellorNoView,
    ArticlePaymentHistory, BookSlotPaymentHistory, 
)

# Register your models here.
@admin.register(CarrerType)
class CarrerTypeAdmin(admin.ModelAdmin):
    list_display = ['typeOfCarrer']

@admin.register(Carrer)
class CarrerAdmin(admin.ModelAdmin):
    list_display = ['carrerType', 'carrer']

@admin.register(CarrerPage)
class CarrerPageAdmin(admin.ModelAdmin):
    list_display = ['carrer', 'heading', 'bannerImage', 'thumbnailImage', 'description']
    
@admin.register(StudentFeaturedArticle)
class StudentFeaturedArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'carrer','title', 'heading', 'description', 'thumbnailImage', 'bannerImage', 'articleApprove', 'createAt']

@admin.register(EditorApproveArticle)
class EditorApproveArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'studentArticle', 'paymentChoices', 'articleApprove', 'ammount', 'rating', 'noView', 'createAt']

@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'editorApproveArticle', 'rating']

@admin.register(ArticleNoView)
class ArticleNoViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'editorApproveArticle', 'noView']

@admin.register(Counsellor)
class CounsellorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'carrer', 'title', 'qualification', 'mobile', 'experience', 'college', 'designation', 'address', 'pincode', 'area', 'aboutUs', 'language', 'price', 'dateOfBirth', 'gender', 'createAt', 'bannerImage', 'rating', 'noView']


@admin.register(CounsellorSlot)
class CounsellorSlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'counsellor', 'date', 'timeFrom', 'timeTo', 'isBook', 'bookedUser']

@admin.register(CounsellorRating)
class CounsellorRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'counsellor', 'rating']


@admin.register(CounsellorNoView)
class CounsellorNoViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'counsellor', 'noView']


@admin.register(BookUserSlot)
class BookUserSlotAdmin(admin.ModelAdmin):
    list_display = ['user', 'counsellorSlot']


@admin.register(ArticlePaymentHistory)
class ArticlePaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'ORDER_ID', 'TXN_AMOUNT', 'email', 'status', 'gateway', 'bankname', 'TXNID', 'TXNDATE', 'CURRENCY', 'PAYMENTMODE', 'MID', 'RESPCODE', 'createAt']

@admin.register(BookSlotPaymentHistory)
class BookSlotPaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'slotBook', 'ORDER_ID', 'TXN_AMOUNT', 'email', 'status', 'gateway', 'bankname', 'TXNID', 'TXNDATE', 'CURRENCY', 'PAYMENTMODE', 'MID', 'RESPCODE', 'createAt']