from rest_framework import serializers

from django.apps import apps


class QuestionSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(many=False, slug_field='name', queryset=apps.get_app_config("masteriqapp").get_model("Category").objects.all())
    class Meta:
        model = apps.get_app_config("masteriqapp").get_model("Question")
        fields = ['text', 'category']