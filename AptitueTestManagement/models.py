from django.db import models

# Create your models here.
class TestScheduleManagement(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # questionsAns = models.ManyToManyField(Career_Cluster, related_name='Career_Cluster')
    duration = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True, auto_created=True)
    amount = models.FloatField(blank=True, null=True)
    testName = models.CharField(blank=True, null=True, max_length=200)
    def __str__(self):
        return str(self.testName)


CATEGORY_CHOICES = (
    ('Agriculture, Food & Natural Resources','Agriculture, Food & Natural Resources'),
    ('Architecture & Construction','Architecture & Construction'),
    ('Arts, A/V Technology & Communications','Arts, A/V Technology & Communications'),
    ('Business Management & Administration','Business Management & Administration'),
    ('Education & Training','Education & Training'),
    ('Finance','Finance'),
    ('Government & Public Administration','Government & Public Administration'),
    ('Health Science','Health Science'),
    ('Hospitality & Tourism','Hospitality & Tourism'),
    ('Human Services','Human Services'),
    ('Information Technology','Information Technology'),
    ('Law, Public Safety, Corrections & Securit','Law, Public Safety, Corrections & Securit'),
    ('Manufacturing','Manufacturing'),
    ('Marketing','Marketing'),
    ('Science, Technology, Engineering & Mathematics','Science, Technology, Engineering & Mathematics'),
    ('Transportation, Distribution & Logistics','Transportation, Distribution & Logistics'),
)


class QuestionManagement(models.Model):
    industry = models.CharField(choices=CATEGORY_CHOICES, max_length=100, null=True)
    question= models.CharField(null=True, blank=True, max_length=200)
    ans1 = models.CharField(null=True, blank=True, max_length=200)
    ans2 = models.CharField(null=True, blank=True, max_length=200)
    ans3 = models.CharField(null=True, blank=True, max_length=200)
    ans4 = models.CharField(null=True, blank=True, max_length=200)
    ans5 = models.CharField(null=True, blank=True, max_length=200)
    # def __str__(self):
    #     return str(self.id)
        
    def __str__(self):
        return str(self.industry)