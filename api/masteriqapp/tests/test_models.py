from django.test import TestCase
import django.apps

from masteriqapp.models import Category
from masteriqapp.models import Iq
from masteriqapp.models import Question
from masteriqapp.models import Option
from django.contrib.auth.models import User


class ModelTestCases(TestCase):
    def test_recognized_models(self):
        """Check if the models are all recognized"""
        models_list = django.apps.apps.get_models()
        models_to_find = (Category, Iq, Question, Option)
        for model in models_to_find:
            assert model in models_list

    def test_use_model(self):
        category_test = Category.objects.create(name="Test")

        question_test = Question.objects.create(text="Yes or No?", category=category_test)

        option_1 = Option.objects.create(text="Yes", is_correct=False, question=question_test)
        option_2 = Option.objects.create(text="No", is_correct=True, question=question_test)

        user_test = User.objects.create_user("test", "test@example.com", "password")

        iq_test = Iq.objects.create(user=user_test, category=category_test, iq=100)

        assert len(Category.objects.filter(name="Test")) == 1
        assert len(Question.objects.filter(text="Yes or No?")) == 1
        assert len(Option.objects.filter(text="Yes")) == 1
        assert len(Option.objects.all()) >= 2
        assert len(User.objects.filter(username="test")) == 1
        assert len(Iq.objects.filter(user=user_test, category=category_test)) == 1




