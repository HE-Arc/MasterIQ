from django.test import TestCase
import django.apps

from masteriqapp.models import Category
from masteriqapp.models import IQ
from masteriqapp.models import Question
from masteriqapp.models import Option
from django.contrib.auth.models import User


class ModelTestCases(TestCase):
    def test_recognized_models(self):
        """Check if the models are all recognized"""
        models_list = django.apps.apps.get_models()
        models_to_find = (Category, IQ, Question, Option)
        for model in models_to_find:
            assert model in models_list

    def test_use_model(self):
        category_test = Category.objects.create(name="Test")

        question_test = Question.objects.create(text="Yes or No?", category=category_test)

        option_1 = Option.objects.create(text="Yes", is_correct=False, question=question_test)
        option_2 = Option.objects.create(text="No", is_correct=True, question=question_test)

        user_test = User.objects.create_user("test", "test@example.com", "password")

        iq_test = IQ.objects.create(user=user_test, category=category_test, iq=100)

        assert len(Category.objects.filter(name="Test")) == 1
        assert len(Question.objects.filter(text="Yes or No?")) == 1
        assert len(Option.objects.filter(text="Yes")) == 1
        assert len(Option.objects.all()) >= 2
        assert len(User.objects.filter(username="test")) == 1
        assert len(IQ.objects.filter(user=user_test, category=category_test)) == 1

    def test_use_manager(self):
        category_test = Category.objects.create(name="test_managers")
        user_test = User.objects.create_user("test_managers", "test_managers@example.com", "password")
        iq_test = IQ.objects.create(user=user_test, category=category_test, iq = 102)

        leaderboard = IQ.objects.get_best_players_of_category(category=category_test)
        iq_cat = IQ.objects.get_iq_of_user_in_category(user=user_test, category=category_test)
        all_iq = IQ.objects.get_all_iq_of_user(user=user_test)
        assert len(leaderboard) >= 1
        assert iq_cat == 102
        assert len(all_iq) == 1
        assert all_iq[0]["iq"] == 102
        assert all_iq[0]["category"] == category_test.id