from django.db import models
from django.conf import settings
import os

class Category(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="IQ")
    image_path = models.CharField(max_length=255, default=os.path.join(settings.IMAGES_FOLDER, settings.DEFAULT_IMAGE))


