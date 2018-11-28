from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=30)
    created_at = models.DateField()