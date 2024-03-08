from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.apps import apps
from PIL import Image
from rest_framework import status
from rest_framework.response import Response

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
