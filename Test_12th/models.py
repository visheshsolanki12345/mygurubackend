from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.
class DefinedGrate(models.Model):
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
    P_11 = models.IntegerField(null=True, blank=True, default=0)
    P_12 = models.IntegerField(null=True, blank=True, default=0)
    P_13 = models.IntegerField(null=True, blank=True, default=0)
    P_14 = models.IntegerField(null=True, blank=True, default=0)
    P_15 = models.IntegerField(null=True, blank=True, default=0)
    grade = models.CharField(null=True, blank=True, max_length=100)
    toFromPair = models.CharField(null=True, blank=True, max_length=100)
    

    def __str__(self):
            return str(self.one)

class DefineClasses(models.Model):
    Class = models.CharField(blank=True, null=True, max_length=200)
    testInstruction = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.Class)

class IndustryCategory(models.Model):
    industry_Id = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.industry)

class Test(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # questionsAns = models.ManyToManyField(Career_Cluster, related_name='Career_Cluster')
    duration = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True, auto_created=True)
    amount = models.FloatField(blank=True, null=True)
    testName = models.CharField(blank=True, null=True, max_length=200)
    grade = models.ForeignKey(DefineClasses,on_delete=CASCADE, blank=True, null=True)
    def __str__(self):
        return str(self.testName)

class Questions(models.Model):
    industry = models.ForeignKey(IndustryCategory,on_delete=CASCADE, max_length=100, null=True, blank=True)
    # grade = models.ForeignKey(DefineClasses,on_delete=CASCADE, max_length=100, null=True, blank=True)
    question= models.TextField(null=True, blank=True)
    a = models.CharField(null=True, blank=True, max_length=300)
    b = models.CharField(null=True, blank=True, max_length=300)
    c = models.CharField(null=True, blank=True, max_length=300)
    d = models.CharField(null=True, blank=True, max_length=300)
    e = models.CharField(null=True, blank=True, max_length=300)
    def __str__(self):
        return str(self.industry)
    
class Interpretation_12th(models.Model):
    grade = models.CharField(max_length=200, null=True, blank=True)
    interpretationTitle = models.TextField(null=True, blank=True)
    YouCanDoPoint_1 = models.CharField(max_length=200, null=True, blank=True)
    YouCanDoPoint_2 = models.CharField(max_length=200, null=True, blank=True)
    YouCanDoPoint_3 = models.CharField(max_length=200, null=True, blank=True)
    YouCanDoPoint_4 = models.CharField(max_length=200, null=True, blank=True)
    YouCanDoPoint_5 = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.id)


class Reports_12th(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, max_length=100, null=True, blank=True)
    interpretatio = models.ForeignKey(Interpretation_12th,on_delete=CASCADE, max_length=500, null=True, blank=True, related_name="interpretatio")
    industry = models.CharField(null=True, blank=True, max_length=200)
    question = models.TextField(null=True, blank=True)
    a = models.IntegerField(null=True, blank=True)
    b = models.IntegerField(null=True, blank=True)
    c = models.IntegerField(null=True, blank=True)
    d = models.IntegerField(null=True, blank=True)
    e = models.IntegerField(null=True, blank=True)
    totalCount = models.IntegerField(null=True, blank=True)
    grade = models.CharField(null=True, blank=True, max_length=100)
    CreateAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    industry_Grade = models.CharField(null=True, blank=True, max_length=200)

    def save(self, *args, **kwargs):
        ResultCount = self.a + self.b + self.c + self.d + self.e
        self.totalCount = ResultCount
        super(Reports_12th, self).save(*args, **kwargs)
       
    def __str__(self):
        return str(self.user)

class ShowGrade(models.Model):
    score = models.CharField( max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.score)


class GeneralInformation_12th(models.Model):
    TitleImportance = models.TextField(null=True, blank=True) 
    VerbalAbility = models.TextField(null=True, blank=True) 
    NumericalAbility = models.TextField(null=True, blank=True) 
    AbstractReasoning = models.TextField(null=True, blank=True) 
    LogicalReasoningAbility = models.TextField(null=True, blank=True) 
    MechanicalAbility = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.id)
    