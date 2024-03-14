from rest_framework import serializers

from django.apps import apps


class QuestionAndOptionsSerializer(serializers.ModelSerializer):
    options = serializers.StringRelatedField(many=True, read_only=True)
    category = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = apps.get_app_config("masteriqapp").get_model("Question")
        fields = ['id', 'text', 'category', 'options']