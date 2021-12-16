from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
import os
# Create your models here.

def user_directory_path_main(instance, filename):
    profile_pic_name = f'profile_picture/{instance.user.username}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    if os.path.exists(full_path):
    	os.remove(full_path)
    return profile_pic_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    className = models.CharField(null=True, blank=True, max_length=100)
    userPic = models.ImageField(upload_to=user_directory_path_main,null=True, blank=True, verbose_name='UserPic')
    
    def __str__(self):
        return str(self.user)