from rest_framework import serializers

from django.apps import apps


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_app_config("masteriqapp").get_model("Question")
        fields = ['id', 'text', 'category']