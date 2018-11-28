from django.db import models

class Temperature(models.Model):
    month = models.CharField(max_length=30)
    date = models.DateField(auto_now=False)
    max = models.IntegerField()
    min = models.IntegerField()
