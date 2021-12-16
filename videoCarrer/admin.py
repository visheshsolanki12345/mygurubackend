from django.contrib import admin
from .models import YouTubeVideo

# Register your models here.
@admin.register(YouTubeVideo)
class YouTubeVideoModelAdmin(admin.ModelAdmin):
    list_display = ['id','videoLink', 'videoTitle', 'description', 'createAt']