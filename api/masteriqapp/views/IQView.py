import random

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

masteriq = apps.get_app_config("masteriqapp")


class IQView(viewsets.ViewSet):
    category_model = masteriq.get_model("Category")
    queryset = category_model.objects.all()

    @action(detail=True, methods=["GET"], url_path="image")
    def category_image(self, request, pk):
        category = get_object_or_404(self.queryset, pk=pk)
        try:
            with open(category.image_path, 'rb') as img:
                return HttpResponse(img.read(), content_type="image/jpeg", status=status.HTTP_200_OK)
        except IOError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["GET"], url_path="iq")
    def category_with_iq(self, request):
        # TODO: RESTRICT TO CONNECTED USER
        answer_dict = {}
        for category in self.queryset:
            cat_dict = {
                "category_name": category.name,
                "user_iq": 100  # TODO: REPLACE WITH USER IQ
            }
            answer_dict[category.id] = cat_dict
        return Response(status=status.HTTP_200_OK, data=answer_dict)

    @action(detail=True, methods=["GET"])
    def user_iq(self, request, pk):
        return Response(status=status.HTTP_200_OK, data={"user_iq": random.randint(1, 200)})

    @action(detail=True, methods=["GET"], url_path="name")
    def category_name(self, request, pk):
        category = get_object_or_404(self.queryset, pk=pk)
        return Response(status=status.HTTP_200_OK, data={"category_name": category.name})
