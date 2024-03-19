from rest_framework import serializers

from django.apps import apps


class OptionSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(many=False, queryset=apps.get_app_config("masteriqapp").get_model("Question").objects.all())
    # question = serializers.SlugRelatedField(many=False, slug_field='id',
    #                                         queryset=apps.get_app_config("masteriqapp").get_model(
    #                                             "Question").objects.all())
    #question_id = serializers.UUIDField()
    class Meta:
        model = apps.get_app_config("masteriqapp").get_model("Option")
        fields = ['text', 'is_correct', 'question']
