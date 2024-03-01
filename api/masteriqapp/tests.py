from django.test import TestCase
import django.apps

from masteriqapp.models import Category
from masteriqapp.models import Iq
from masteriqapp.models import Question
from masteriqapp.models import Option


# Create your tests here.
class ModelTestCases(TestCase):
    def test_recognized_models(self):
        """Check if the models are all recognized"""
        models_list = django.apps.apps.get_models()
        models_to_find = (Category, Iq, Question, Option)
        for model in models_to_find:
            assert model in models_list
