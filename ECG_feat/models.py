from django.db import models

# Create your models here.

class ECG_model(models.Model):
    user_name = models.CharField(max_length= 200, null= True)
    signal_x = models.CharField(max_length= 200, null= True)
    signla_y = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.user_name