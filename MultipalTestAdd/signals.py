from django.dispatch import receiver, Signal
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete
from .models import ImageOptionsTest


@receiver(post_save, sender=ImageOptionsTest)
def at_ending_save(sender, instance, created ,**kwargs):
    print('....................', created)
    if created:
        rightAns = ''
        obj = ImageOptionsTest.objects.get(id = instance.id)
        choiceRightAns = obj.choiceRightAns
        if choiceRightAns == 'A':
            rightAns = f"/media/{obj.a}"
        elif choiceRightAns == 'AText':
            rightAns = obj.aText
        elif choiceRightAns == 'B':
            rightAns = f"/media/{obj.b}"
        elif choiceRightAns == 'BText':
            rightAns = obj.bText
        elif choiceRightAns == 'C':
            rightAns = f"/media/{obj.c}"
        elif choiceRightAns == 'CText':
            rightAns = obj.cText
        elif choiceRightAns == 'D':
            rightAns = f"/media/{obj.d}"
        elif choiceRightAns == 'DText':
            rightAns = obj.dText
        elif choiceRightAns == 'E':
            rightAns = f"/media/{obj.e}"
        elif choiceRightAns == 'EText':
            rightAns = obj.eText
        obj.rightAns = rightAns
        obj.save()
    else:
        rightAns = ''
        objMy = ImageOptionsTest.objects.filter(id = instance.id)
        for obj in objMy:
            choiceRightAns = obj.choiceRightAns
            if choiceRightAns == 'A':
                rightAns = f"/media/{obj.a}"
            elif choiceRightAns == 'AText':
                rightAns = obj.aText
            elif choiceRightAns == 'B':
                rightAns = f"/media/{obj.b}"
            elif choiceRightAns == 'BText':
                rightAns = obj.bText
            elif choiceRightAns == 'C':
                rightAns = f"/media/{obj.c}"
            elif choiceRightAns == 'CText':
                rightAns = obj.cText
            elif choiceRightAns == 'D':
                rightAns = f"/media/{obj.d}"
            elif choiceRightAns == 'DText':
                rightAns = obj.dText
            elif choiceRightAns == 'E':
                rightAns = f"/media/{obj.e}"
            elif choiceRightAns == 'EText':
                rightAns = obj.eText
        objMy.update(rightAns = rightAns)

