from django.db import models
from masteriqapp.models.Category import Category


class Question(models.Model):
    text = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
