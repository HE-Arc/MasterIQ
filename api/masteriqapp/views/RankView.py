import random

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Window, F, Subquery, Avg
from django.db.models.functions import RowNumber
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

masteriq = apps.get_app_config("masteriqapp")


class RankView(viewsets.ViewSet):
    category_model = masteriq.get_model("Category")
    question_model = masteriq.get_model("Question")
    user_model = get_user_model()
    iq_model = masteriq.get_model("IQ")
    queryset = category_model.objects.all()
    permission_classes = (IsAuthenticated,)
    @action(detail=True, methods=["GET"])
    def leaderboard(self, request, pk):
        data_to_send = []
        category = self.category_model.objects.get(pk=pk)
        best_iqs = self.iq_model.objects.get_best_players_of_category(category=category)
        for iq in best_iqs:
            user = iq.user
            data_to_send.append({
                "user_id": user.id,
                "user_name": user.username,
                "user_iq": iq.iq
            })

        return Response(data=data_to_send, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def global_leaderboard(self, request):
        data_with_score = get_user_model().objects.annotate(global_score=Avg('iq__iq')).order_by('-global_score',)[:10]
        data_to_send = []
        for user in data_with_score:
            data_to_send.append({
                "user_id": user.id,
                "user_name": user.username,
                "user_iq": user.global_score
            })

        return Response(data=data_to_send, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def user(self, request, pk):
        #TODO: ask how to do better?? filter won't be efficient if more element
        category = self.category_model.objects.get(pk=pk)
        ranking = self.iq_model.objects.annotate(row_number=Window(expression=RowNumber(), order_by=F('iq').desc())).filter(category=category).values('iq', 'user_id', 'row_number', 'category_id')
        user_ranking = list(filter(lambda r: r['user_id'] == request.user.id, ranking))
        iq = self.iq_model.objects.get(user=request.user, category=category)
        data_to_send = {"user_rank": user_ranking[0]['row_number'], "user_iq": iq.iq}
        return Response(data=data_to_send, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def global_user(self, request):
        # TODO: ask how to do better?? filter won't be efficient if more element
        data_with_score = get_user_model().objects.annotate(global_score=Avg('iq__iq'), row_number=Window(expression=RowNumber())).order_by('-global_score')
        user_ranking = list(filter(lambda r: r.id == request.user.id, data_with_score))
        data_to_send = {"user_rank": user_ranking[0].row_number, "user_iq": user_ranking[0].global_score}
        return Response(data=data_to_send, status=status.HTTP_200_OK)
