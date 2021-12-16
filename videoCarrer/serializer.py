
from rest_framework import serializers
from .models import YouTubeVideo


class YouTubeVideoSerializer(serializers.ModelSerializer):
    createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = YouTubeVideo
        fields = ['id','videoLink', 'videoTitle', 'description', 'createAt']