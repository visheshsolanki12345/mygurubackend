from django.db import models

# Create your models here.
class CheckForPaymentId(models.Model):
    _id = models.UUIDField()
    forPayment = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return str(f"{self.forPayment} - {self._id}")