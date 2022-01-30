from django.db import models
from django.db.models.deletion import CASCADE
from PIL import Image
from django.conf import settings
import os

# Create your models here.
class CareerCategory(models.Model):
    industry = models.CharField(null=True, blank=True, max_length=400)

    def __str__(self):
        return str(self.industry)

def Banner_directory_path_main(instance, filename):
    profile_pic_name = f'Banner_Images/{instance.industry}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_pic_name

class Course(models.Model):
    industry = models.ForeignKey(CareerCategory, null=True, blank=True, on_delete=CASCADE, related_name='industryData')
    courseName = models.CharField(max_length=500, null=True, blank=True)
    bannerImage = models.ImageField(upload_to=Banner_directory_path_main,null=True, blank=True)
    bannerImage2 = models.ImageField(upload_to=Banner_directory_path_main,null=True, blank=True)

    def __str__(self):
        return str(self.industry)
