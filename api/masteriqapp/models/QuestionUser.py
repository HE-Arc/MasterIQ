from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from masteriqapp.models import Question


class QuestionUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options_asked = models.BooleanField(default=False)