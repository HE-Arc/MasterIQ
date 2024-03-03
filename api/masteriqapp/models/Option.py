from django.db import models
from masteriqapp.models.Question import Question


class Option(models.Model):
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)