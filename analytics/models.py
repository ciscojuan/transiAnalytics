from django.db import models

class Temperature(models.Model):
    month = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    max = models.IntegerField()
    min = models.IntegerField()
