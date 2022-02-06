from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.utils.timesince import timesince
        


# Create your models here.
def Banner_directory_path_main(instance, filename):
    bannerImage = f'Banner_Images/{instance.carrer}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, bannerImage)
    if os.path.exists(full_path):
        os.remove(full_path)
    return bannerImage

def student_featured_article(instance, filename):
    articalImage = f'articles/{instance.carrer}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, articalImage)
    if os.path.exists(full_path):
        os.remove(full_path)
    return articalImage

def counsellor_carrer(instance, filename):
    counsellorImage = f'counsellorImage/{instance.carrer}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, counsellorImage)
    if os.path.exists(full_path):
        os.remove(full_path)
    return counsellorImage


class CarrerType(models.Model):
    typeOfCarrer = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return str(self.typeOfCarrer)


class Carrer(models.Model):
    carrerType = models.ForeignKey(CarrerType, null=True, blank=True, on_delete=CASCADE)
    carrer = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return str(f"{self.carrerType} - {self.carrer}")


class CarrerPage(models.Model):
    carrer = models.ForeignKey(Carrer, null=True, blank=True, on_delete=CASCADE)
    heading = models.CharField(max_length=400, null=True, blank=True)
    bannerImage  = models.ImageField(upload_to=Banner_directory_path_main,null=True, blank=True)
    thumbnailImage  = models.ImageField(upload_to=Banner_directory_path_main,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.carrer)


class StudentFeaturedArticle(models.Model):
    user  = models.OneToOneField(User, null=True, blank=True, on_delete=CASCADE)
    carrer = models.ForeignKey(Carrer, null=True, blank=True, on_delete=CASCADE)
    title = models.CharField(max_length=400, null=True, blank=True)
    heading = models.CharField(max_length=500, null=True, blank=True)   
    description = models.TextField(null=True, blank=True)
    thumbnailImage  = models.ImageField(upload_to=student_featured_article,null=True, blank=True)
    bannerImage  = models.ImageField(upload_to=student_featured_article,null=True, blank=True)
    articleApprove = models.CharField(max_length=400, null=True, blank=True, default="Panding")
    createAt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(f"{self.user} - {self.carrer}")


PAYMENT_CHOICES =(
    ("Paid", "Paid"),
    ("Free", "Free"),
)

ARTICLE_APPROVE_CHOICES =(
    ("Approved", "Approved"),
    ("Declined", "Declined"),
)


class EditorApproveArticle(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    carrer = models.ForeignKey(Carrer, null=True, blank=True, on_delete=CASCADE)
    studentArticle = models.ForeignKey(StudentFeaturedArticle, null=True, blank=True, on_delete=CASCADE)
    paymentChoices = models.CharField(choices = PAYMENT_CHOICES, max_length=400, null=True, blank=True)
    articleApprove = models.CharField(choices = ARTICLE_APPROVE_CHOICES, max_length=400, null=True, blank=True)
    ammount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    rating = models.FloatField(null=True, blank=True, default=0)
    noView = models.IntegerField(null=True, blank=True, default=0)
    
    createAt = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        StudentFeaturedArticle.objects.filter(id = self.studentArticle.id).update(articleApprove = self.articleApprove)
        objCarrer = Carrer.objects.get(id = self.studentArticle.carrer.id)
        self.carrer = objCarrer
        super(EditorApproveArticle, self).save(*args, **kwargs)
    def __str__(self):
        return str(f"{self.user} - {self.studentArticle}")

class ArticleRating(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    editorApproveArticle = models.ForeignKey(EditorApproveArticle, null=True, blank=True, on_delete=CASCADE, related_name="articleByRating")
    rating = models.FloatField(null=True, blank=True, default=0)
    def __str__(self):
        return str(f"{self.user} - {self.editorApproveArticle}")

class ArticleNoView(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    editorApproveArticle = models.ForeignKey(EditorApproveArticle, null=True, blank=True, on_delete=CASCADE, related_name="noViewArticle")
    noView = models.IntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return str(f"{self.user} - {self.editorApproveArticle}")

class ArticlePaymentHistory(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,max_length=400, null=True, blank=True)
    article = models.ForeignKey(EditorApproveArticle,on_delete=CASCADE,max_length=400, null=True, blank=True)                   
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
        return str(f"{self.user} - {self.article}" )



class Counsellor(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    carrer = models.ForeignKey(Carrer, null=True, blank=True, on_delete=CASCADE)
    title = models.TextField(null=True, blank=True)
    qualification = models.TextField(null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    college = models.TextField(null=True, blank=True)
    designation = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    area = models.TextField(null=True, blank=True)
    aboutUs = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=400,null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    dateOfBirth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=200,null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    bannerImage  = models.ImageField(upload_to=counsellor_carrer,null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, default=0)
    noView = models.IntegerField(null=True, blank=True, default=0)
    
    def __str__(self):
        return str(f"{self.user} - {self.carrer}")


class CounsellorRating(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    counsellor = models.ForeignKey(Counsellor, null=True, blank=True, on_delete=CASCADE)
    rating = models.FloatField(null=True, blank=True, default=0)
    def __str__(self):
        return str(f"{self.user} - {self.counsellor}")

class CounsellorNoView(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    counsellor = models.ForeignKey(Counsellor, null=True, blank=True, on_delete=CASCADE)
    noView = models.IntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return str(f"{self.user} - {self.counsellor}")


class CounsellorSlot(models.Model):
    counsellor = models.ForeignKey(Counsellor, null=True, blank=True, on_delete=CASCADE)
    date  = models.DateField(auto_created=False, null=True, blank=True)
    timeFrom  = models.TimeField(auto_created=False, null=True, blank=True)
    timeTo  = models.TimeField(auto_created=False, null=True, blank=True)
    isBook = models.BooleanField(default=False)
    bookedUser = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True) 
    def __str__(self):
        return str(self.counsellor)


class BookUserSlot(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    counsellorSlot = models.ForeignKey(CounsellorSlot, null=True, blank=True, on_delete=CASCADE)
    
    def __str__(self):
        return str(f"{self.user} - {self.counsellorSlot}")


class BookSlotPaymentHistory(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,max_length=400, null=True, blank=True)
    slotBook = models.ForeignKey(BookUserSlot,on_delete=CASCADE,max_length=400, null=True, blank=True)                   
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
        return str(f"{self.user} - {self.slotBook}" )