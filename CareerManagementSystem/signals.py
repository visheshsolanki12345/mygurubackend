from django.contrib.auth.models import User
from django.dispatch import receiver, Signal
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete
from .models import BookUserSlot, CounsellorSlot
import time
from django.core.mail import send_mail


@receiver(post_save, sender=BookUserSlot)
def at_ending_save(sender, instance, created ,**kwargs):
    if created:
        CounsellorSlot.objects.filter(id = instance.counsellorSlot.id).update(isBook = True, bookedUser = instance.user)

        # email_plaintext_message = f"Your Slot booking \n "
        # send_mail(
        #     # title:
        #     "Password Reset for {title}".format(title="myGuru's Test"),
        #     # message:
        #     email_plaintext_message,
        #     # from:
        #     "visheshsolanki12345@gmail.com",
        #     # to:
        #     [instance.counsellor.email]
        # )

    else:
        print('...............................')
