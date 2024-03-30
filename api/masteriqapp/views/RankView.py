import random

from django.apps import apps
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

masteriq = apps.get_app_config("masteriqapp")


class RankView(viewsets.ViewSet):
    category_model = masteriq.get_model("Category")
    question_model = masteriq.get_model("Question")
    queryset = category_model.objects.all()

    @action(detail=True, methods=["GET"])
    def leaderboard(self, request, pk):
        # TODO: get data from database when users are implemented
        data_to_send = []
        for i in range(1, 11):
            data_to_send.append({
                "user_id": random.randint(1, 1000),
                "user_name": f"player_number_{i}",
                "user_iq": 150 - (i * 10)
            })

        return Response(data=data_to_send, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def global_leaderboard(self, request):
        # TODO: get data from database when users are implemented
        data_to_send = []
        for i in range(1, 11):
            data_to_send.append({
                "user_id": random.randint(1, 1000),
                "user_name": f"player_number_{i}",
                "user_iq": 50 + (i * 10)
            })

        return Response(data=data_to_send, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def user(self, request, pk):
        # TODO: get data from database when users are implemented

        data_to_send = {"user_rank": random.randint(1, 1000), "user_iq": random.randint(1, 200)}
        return Response(data=data_to_send, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def global_user(self, request):
        # TODO: get data from database when users are implemented
        data_to_send = {"user_rank": random.randint(1, 1000), "user_iq": random.randint(1, 200)}
        return Response(data=data_to_send, status=status.HTTP_200_OK)
