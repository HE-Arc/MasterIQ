from django.apps import apps
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

import masteriqapp.models.IQ

masteriq = apps.get_app_config("masteriqapp")

class AuthenticationView(viewsets.ViewSet):
    category_model = masteriq.get_model("Category")
    iq_model = masteriq.get_model("IQ")
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not get_user_model().objects.filter(username=username).exists():
            user = get_user_model().objects.create_user(username=username, password=password)
            self.create_iq_objects_for_new_user(user)
            login(request, user)
            return Response({'message': 'Register successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    def create_iq_objects_for_new_user(self, user):
        categories = self.category_model.objects.all()
        for category in categories:
            try:
                already_existing_entry = self.iq_model.objects.get_iq_of_user_in_category(user=user, category=category)
                print(already_existing_entry)
            except masteriqapp.models.IQ.DoesNotExist:
                self.iq_model.objects.create(user=user, category=category, iq=100)

