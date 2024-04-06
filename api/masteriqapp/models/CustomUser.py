from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    iqs = models.ManyToManyField(settings.AUTH_USER_MODEL, through="IQ")