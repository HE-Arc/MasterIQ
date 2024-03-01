from django.db import models
from django.conf import settings
from masteriqapp.models.Category import Category


class IQ(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    iq = models.IntegerField()

    def get_best_players_of_category(self, category, nb_players):
        return self.objects.filter(category=category).order_by('iq')[:nb_players]