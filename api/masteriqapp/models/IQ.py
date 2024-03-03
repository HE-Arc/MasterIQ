from django.db import models
from django.conf import settings
from masteriqapp.models.Category import Category

class IQManager(models.Manager):
    def get_best_players_of_category(self, category, nb_players=10):
        return self.filter(category=category).order_by('iq')[:nb_players]

    def get_all_iq_of_user(self, user):
        return self.filter(user=user).values("iq", "category")

    def get_iq_of_user_in_category(self, user, category):
        return self.get(user=user, category=category).iq

class IQ(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    iq = models.IntegerField()
    objects = IQManager()

