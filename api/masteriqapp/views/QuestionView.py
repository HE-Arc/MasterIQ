import io
import random

from rest_framework import viewsets
from rest_framework.decorators import action
from django.apps import apps
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from masteriqapp.serializers.QuestionAndOptionsSerializer import QuestionAndOptionsSerializer
from masteriqapp.serializers.QuestionSerializer import QuestionSerializer

masteriq = apps.get_app_config("masteriqapp")

class QuestionView(viewsets.ViewSet):
    category_model = masteriq.get_model("Category")
    question_model = masteriq.get_model("Question")
    queryset = category_model.objects.all()

    @action(detail=True, methods=["GET"])
    def new(self, request, pk):
        category = get_object_or_404(self.queryset, pk=pk)
        if 'question' in request.session:
            actual_question = self.question_model.objects.get(pk=request.session['question'])
            if actual_question.category == category:
                serializer = QuestionSerializer(actual_question)
                return Response(serializer.data, status=status.HTTP_200_OK)

        questions = self.question_model.objects.filter(category=category)
        new_question = random.choice(questions)
        request.session['question'] = new_question.id
        print(request.session['question'])
        serializer = QuestionSerializer(new_question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def new_community(self, request):
        datas = request.data
        if not ('question' in datas and 'answer' in datas and 'options' in datas):
            print("bad 1")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if len(datas['options']) < 1:
            print("bad 2")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        category = self.category_model.objects.get(name="Community")
        question = self.question_model.objects.create(text=datas['question'], category=category)
        options = []
        for option in datas['options']:
            options.append(masteriq.get_model('Option').objects.create(text=option, is_correct=False, question=question))
        options.append(masteriq.get_model('Option').objects.create(text=datas['answer'], is_correct=True, question=question))

        question_serializer = QuestionAndOptionsSerializer(question)

        return Response(question_serializer.data, status=status.HTTP_201_CREATED)