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