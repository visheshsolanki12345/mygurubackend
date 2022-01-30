from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
import os
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
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


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = f"https://my-guru-test.herokuapp.com/password-reset/{reset_password_token.key}"
    # email_plaintext_message = f"http://localhost:3000/password-reset/{reset_password_token.key}"

    send_mail(
        # title:
        "Password Reset for {title}".format(title="myGuru's Test"),
        # message:
        email_plaintext_message,
        # from:
        "visheshsolanki12345@gmail.com",
        # to:
        [reset_password_token.user.email]
    )