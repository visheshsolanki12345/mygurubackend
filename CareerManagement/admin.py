from django.contrib import admin

from .models  import Industry
# Register your models here.
# admin.site.register(Industry)
@admin.register(Industry)
class IndustryModelAdmin(admin.ModelAdmin):
    list_display = ['category', 'id','qution']