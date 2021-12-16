from django.contrib import admin
from .models import CareerCategory, Course
# Register your models here.
@admin.register(CareerCategory)
class CareerCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'industry']

@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'industry', 'courseName', 'bannerImage']
