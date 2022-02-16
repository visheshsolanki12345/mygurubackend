from operator import mod
from django.db import models
from django.contrib.auth.models import User
from CareerManagementSystem.models import Carrer
from django.db.models.deletion import CASCADE
from django.conf import settings
import os

# Create your models here.

def video_carrer(instance, filename):
    videoImage = f'videoBanner/{instance.carrer}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, videoImage)
    if os.path.exists(full_path):
        os.remove(full_path)
    return videoImage

class YouTubeVideo(models.Model):
    videoLink = models.URLField(max_length=400, null=True, blank=True)
    videoTitle = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    createAt = models.DateTimeField( auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return str(self.videoTitle)


PAYMENT_CHOICES =(
    ("Paid", "Paid"),
    ("Free", "Free"),
)

class VideoCarrer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    carrer = models.ForeignKey(Carrer, null=True, blank=True, on_delete=CASCADE)
    title = models.CharField(max_length=400,null=True, blank=True)
    sortDescription = models.TextField(null=True, blank=True)
    embedUrl = models.URLField(max_length = 500, null=True, blank=True)
    earnings = models.CharField(choices = PAYMENT_CHOICES, max_length=400, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, default=0)
    noView = models.IntegerField(null=True, blank=True, default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    hide = models.BooleanField(default=False)
    thumbnailImage  = models.ImageField(upload_to=video_carrer,null=True, blank=True)

    
    def __str__(self):
        return str(self.carrer)

class VideoPaymentHistory(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,max_length=400, null=True, blank=True)
    video = models.ForeignKey(VideoCarrer,on_delete=CASCADE,max_length=400, null=True, blank=True)                   
    ORDER_ID = models.CharField(max_length=400, null=True, blank=True)
    TXN_AMOUNT = models.CharField(max_length=400, null=True, blank=True)
    email = models.CharField(max_length=400, null=True, blank=True)
    status = models.CharField(max_length=400, null=True, blank=True)
    gateway = models.CharField(max_length=400, null=True, blank=True)
    bankname = models.CharField(max_length=400, null=True, blank=True)
    TXNID = models.CharField(max_length=400, null=True, blank=True)
    TXNDATE = models.CharField(max_length=400, null=True, blank=True)
    RESPCODE = models.CharField(max_length=400, null=True, blank=True)
    CURRENCY = models.CharField(max_length=400, null=True, blank=True)
    PAYMENTMODE = models.CharField(max_length=400, null=True, blank=True)
    MID = models.CharField(max_length=400, null=True, blank=True)
    createAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} - {self.video}" )

class VideoRating(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    videoCarrer = models.ForeignKey(VideoCarrer, null=True, blank=True, on_delete=CASCADE, related_name="videoByRating")
    rating = models.FloatField(null=True, blank=True, default=0)
    def __str__(self):
        return str(f"{self.user} - {self.videoCarrer}")

class VideoNoView(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    videoCarrer = models.ForeignKey(VideoCarrer, null=True, blank=True, on_delete=CASCADE, related_name="videoNoView")
    noView = models.IntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return str(f"{self.user} - {self.videoCarrer}")
