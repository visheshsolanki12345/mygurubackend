from django.db import models

# Create your models here.

class YouTubeVideo(models.Model):
    videoLink = models.CharField(max_length=300, null=True, blank=True)
    videoTitle = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    createAt = models.DateTimeField( auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return str(self.videoTitle)



        
