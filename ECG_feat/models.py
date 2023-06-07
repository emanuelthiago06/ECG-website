from django.db import models

# Create your models here.

class ECG_model(models.Model):
    amp = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return f"{self.amp} "


class ECG_models(models.Model):
    amp = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return f"{self.amp} "