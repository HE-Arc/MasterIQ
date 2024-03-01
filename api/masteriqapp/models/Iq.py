from django.db import models
from django.conf import settings
from masteriqapp.models.Category import Category
class Iq(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    iq = models.IntegerField()