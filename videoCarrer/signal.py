from django.contrib.auth.models import User
from django.dispatch import receiver, Signal
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete
from .models import VideoRating, VideoNoView, VideoCarrer
from .import views

