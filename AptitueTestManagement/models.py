from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

# Create your models here.

class TestScheduleManagement(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # questionsAns = models.ManyToManyField(Career_Cluster, related_name='Career_Cluster')
    duration = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True, auto_created=True)
    amount = models.FloatField(blank=True, null=True)
    testName = models.CharField(blank=True, null=True, max_length=200)
    grade = models.CharField(max_length=200 ,blank=True, null=True)
    def __str__(self):
        return str(self.testName)


class IndustryCategory(models.Model):
    industry_Id = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.industry)


class QuestionManagement(models.Model):
    industry = models.ForeignKey(IndustryCategory,on_delete=CASCADE, max_length=100, null=True, blank=True)
    question= models.TextField(null=True, blank=True)
    a = models.CharField(null=True, blank=True, max_length=200)
    b = models.CharField(null=True, blank=True, max_length=200)
    c = models.CharField(null=True, blank=True, max_length=200)
    d = models.CharField(null=True, blank=True, max_length=200)
    e = models.CharField(null=True, blank=True, max_length=200)
    def __str__(self):
        return str(self.industry)
    

class DefinedTestGrate(models.Model):
    one = models.IntegerField(null=True, blank=True, default=0)
    two = models.IntegerField(null=True, blank=True, default=0)
    three = models.IntegerField(null=True, blank=True, default=0)
    four = models.IntegerField(null=True, blank=True, default=0)
    five =  models.IntegerField(null=True, blank=True, default=0)
    six = models.IntegerField(null=True, blank=True, default=0)
    seven = models.IntegerField(null=True, blank=True, default=0)
    eight = models.IntegerField(null=True, blank=True, default=0)
    nine =  models.IntegerField(null=True, blank=True, default=0)
    ten = models.IntegerField(null=True, blank=True, default=0)
    grade = models.CharField(null=True, blank=True, max_length=100)
    toFromPair = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
            return str(self.one)


class TestResult(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, max_length=100, null=True, blank=True)
    industry = models.CharField(null=True, blank=True, max_length=200)
    question = models.CharField(null=True, blank=True, max_length=200)
    ans1 = models.IntegerField(null=True, blank=True)
    ans2 = models.IntegerField(null=True, blank=True)
    ans3 = models.IntegerField(null=True, blank=True)
    ans4 = models.IntegerField(null=True, blank=True)
    ans5 = models.IntegerField(null=True, blank=True)
    totalCount = models.IntegerField(null=True, blank=True)
    grade = models.CharField(null=True, blank=True, max_length=100)
    CreateAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    industry_Grade = models.CharField(null=True, blank=True, max_length=200)

    def save(self, *args, **kwargs):
        ResultCount = self.ans1 + self.ans2 + self.ans3 + self.ans4 + self.ans5
        self.totalCount = ResultCount
        super(TestResult, self).save(*args, **kwargs)
       
    def __str__(self):
        return str(self.user)

class ShowGrade(models.Model):
    score = models.CharField( max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.score)
