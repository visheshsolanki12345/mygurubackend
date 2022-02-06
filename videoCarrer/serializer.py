
from rest_framework import serializers

from authentication.serializer import userCustomSerializer
from CareerManagementSystem.serializer import CarrerSerializer
from .models import YouTubeVideo, VideoCarrer, VideoRating, VideoNoView


class YouTubeVideoSerializer(serializers.ModelSerializer):
    createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = YouTubeVideo
        fields = ['id','videoLink', 'videoTitle', 'description', 'createAt']



class VideoCarrerSerializer(serializers.ModelSerializer):
    # createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    user = userCustomSerializer(many=False, read_only=True)
    carrer = CarrerSerializer(many=False, read_only=True)
    class Meta:
        model = VideoCarrer
        fields = ['id','user', 'carrer', 'title', 'sortDescription', 'thumbnailImage', 'embedUrl', 'earnings', 'price', 'rating', 'noView','createAt']