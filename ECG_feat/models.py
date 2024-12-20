from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ECG_model(models.Model):
    amp = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return f"{self.amp} "


class ECG_models(models.Model):
    key = models.IntegerField()
    amp = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return f"{self.amp} "
    

class vcg_model(models.Model):
    key = models.IntegerField()
    amp_1 = models.FloatField()
    amp_2 = models.FloatField()
    amp_3 = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering=['pk']