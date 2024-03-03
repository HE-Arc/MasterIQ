from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="IQ")

