from datetime import datetime, timedelta

import pytz
from django.apps import apps
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.conf import settings

import masteriqapp.models.IQ

masteriq = apps.get_app_config("masteriqapp")


class AuthenticationView(viewsets.ViewSet, ObtainAuthToken):
    category_model = masteriq.get_model("Category")
    iq_model = masteriq.get_model("IQ")

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not get_user_model().objects.filter(username=username).exists():
            user = get_user_model().objects.create_user(username=username, password=password)
            self.create_iq_objects_for_new_user(user)
            return Response({'message': 'Register successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def token(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            if not created:
                # This is required for the time comparison
                utc_now = datetime.utcnow()
                utc_now = utc_now.replace(tzinfo=pytz.utc)

                if token.created < utc_now - timedelta(hours=settings.TOKEN_TIME_BEFORE_EXPIRATION_HOUR):
                    token.delete()
                    token = Token.objects.create(user=serializer.validated_data['user'])

            expiring_date = token.created + timedelta(hours=settings.TOKEN_TIME_BEFORE_EXPIRATION_HOUR)
            return Response({
                'token': token.key,
                'expires': expiring_date
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def create_iq_objects_for_new_user(self, user):
        categories = self.category_model.objects.all()
        for category in categories:
            try:
                already_existing_entry = self.iq_model.objects.get_iq_of_user_in_category(user=user, category=category)
            except masteriqapp.models.IQ.DoesNotExist:
                self.iq_model.objects.create(user=user, category=category, iq=100)
