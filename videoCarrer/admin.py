from django.contrib import admin
from .models import (
    YouTubeVideo, VideoCarrer, VideoRating, VideoNoView
)

# Register your models here.
# @admin.register(YouTubeVideo)
# class YouTubeVideoModelAdmin(admin.ModelAdmin):
#     list_display = ['id','videoLink', 'videoTitle', 'description', 'createAt']


@admin.register(VideoCarrer)
class VideoCarrerAdmin(admin.ModelAdmin):
    list_display = ['user', 'carrer', 'title', 'sortDescription', 'thumbnailImage', 'embedUrl', 'earnings', 'price', 'hide', 'rating', 'noView', 'createAt']
    

# @admin.register(VideoRating)
# class VideoRatingAdmin(admin.ModelAdmin):
#     list_display = ['user', 'videoCarrer', 'rating']


# @admin.register(VideoNoView)
# class ArticleNoViewAdmin(admin.ModelAdmin):
#     list_display = ['user', 'videoCarrer', 'noView']
