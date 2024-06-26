import io
import random
import jellyfish
from rest_framework import viewsets
from rest_framework.decorators import action
from django.apps import apps
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from masteriqapp.serializers.OptionSerializer import OptionSerializer
from masteriqapp.serializers.QuestionAndOptionsSerializer import QuestionAndOptionsSerializer
from masteriqapp.serializers.QuestionSerializer import QuestionSerializer

masteriq = apps.get_app_config("masteriqapp")


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_if_text_answer_is_correct(given_answer, right_answer):
    if (right_answer.lower() == "yes" or right_answer.lower() == "true" or right_answer.lower() == "right") and (
            given_answer.lower() == "yes" or given_answer.lower() == "true" or given_answer.lower() == "right"):
        return True
    if (right_answer.lower() == "no" or right_answer.lower() == "wrong" or right_answer.lower() == "false") and (
            given_answer.lower() == "no" or given_answer.lower() == "wrong" or given_answer.lower() == "false"):
        return True
    if is_number(right_answer):
        if given_answer == right_answer:
            return True
    elif jellyfish.damerau_levenshtein_distance(given_answer.lower(), right_answer.lower()) < 3:
        return True
    return False


class QuestionView(viewsets.ViewSet):
    WRONG_PENALTY = 5
    TEXT_RIGHT_POINTS = 5
    OPTIONS_RIGHT_POINTS = 3
    category_model = masteriq.get_model("Category")
    question_model = masteriq.get_model("Question")
    option_model = masteriq.get_model("Option")
    question_user_model = masteriq.get_model("QuestionUser")
    iq_model = masteriq.get_model("IQ")
    queryset = category_model.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def new(self, request, pk):
        category = get_object_or_404(self.queryset, pk=pk)
        actual_question = request.user.questions.filter(category=category).first()
        if actual_question is not None and actual_question.category == category:
            serializer = QuestionSerializer(actual_question)
            return Response(serializer.data, status=status.HTTP_200_OK)

        questions = self.question_model.objects.filter(category=category)
        if len(questions) == 0:
            return Response({"error":"No questions in this category"}, status=status.HTTP_404_NOT_FOUND)
        new_question = random.choice(questions)
        new_question_user = self.question_user_model(user=request.user, question=new_question, options_asked=False)
        new_question_user.save()
        serializer = QuestionSerializer(new_question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def new_community(self, request):
        datas = request.data
        if not ('question' in datas and 'answer' in datas and 'options' in datas):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if len(datas['options']) < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        category = self.category_model.objects.get(name="Community")
        question_serializer = QuestionSerializer(data={"text": datas["question"], "category": category.name})
        question = None
        if question_serializer.is_valid():
            question = question_serializer.save()
        else:
            return Response(data={"field": "Question", "errors": question_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        options = []
        for i in range(len(datas['options'])):
            if i == int(datas['answer']):
                options.append([datas['options'][i], True])
            else:
                options.append([datas['options'][i], False])
        random.shuffle(options)
        for option in options:
            option_serializer = OptionSerializer(data={"text": option[0], "is_correct": option[1], "question":  question.id})

            if option_serializer.is_valid():
                option_serializer.save()
            else:
                field = "Option"
                if option[1]:
                    field = "Answer"
                return Response(data={"field": field, "error": option_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(question_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def options(self, request, pk):
        category = get_object_or_404(self.queryset, pk=pk)
        actual_question = self.question_user_model.objects.filter(question__category=category, user=request.user).first()
        if actual_question is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No question being answered at the moment in this category"})
        actual_question.options_asked = True
        actual_question.save()
        question = self.question_model.objects.get(pk=actual_question.question_id)
        data_to_send = {'question_id': question.id, 'number_of_options': len(question.options.all()), 'options': {}}
        for option in question.options.all():
            data_to_send['options'][option.id] = option.text
        return Response(status=status.HTTP_200_OK, data=data_to_send)

    @action(detail=True, methods=["POST"], url_path="answer_text", permission_classes=[IsAuthenticated])
    def answer_text(self, request, pk):
        if not 'answer' in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No answer given"})
        category = get_object_or_404(self.queryset, pk=pk)
        actual_question = self.question_user_model.objects.filter(question__category=category, user=request.user).first()
        if actual_question is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No question being answered at the moment in this category"})
        if actual_question.options_asked:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Options already asked, you can only "
                                                                               "answer with options"})
        question = actual_question.question
        right_answer = question.options.get(is_correct=True)
        user_is_correct = check_if_text_answer_is_correct(request.data['answer'], right_answer.text)
        iq = self.iq_model.objects.get(user=request.user, category=question.category)
        if request.data['answer'].lower() == right_answer.text.lower():
            user_is_correct = True
            iq.iq += self.TEXT_RIGHT_POINTS
        else:
            iq.iq -= self.WRONG_PENALTY
        iq.save()
        data_to_send = {"user_is_correct": user_is_correct, "right_answer": right_answer.text,
                        "answer_sent": request.data['answer']}
        actual_question.delete()
        return Response(status=status.HTTP_200_OK, data=data_to_send)

    @action(detail=True, methods=["POST"], url_path="answer_option", permission_classes=[IsAuthenticated])
    def answer_options(self, request, pk):
        if not 'answer' in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No answer given"})
        category = get_object_or_404(self.queryset, pk=pk)
        actual_question = self.question_user_model.objects.filter(question__category=category,
                                                                  user=request.user).first()
        if actual_question is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "No question being answered at the moment in this category"})
        if not actual_question.options_asked:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "Options already asked, you can only "
                                           "answer with options"})
        question = actual_question.question
        right_answer = question.options.get(is_correct=True)
        answer_sent = self.option_model.objects.get(pk=request.data['answer'])
        user_is_correct = False
        iq = self.iq_model.objects.get(user=request.user, category=question.category)
        if answer_sent.id == right_answer.id:
            user_is_correct = True
            iq.iq += self.OPTIONS_RIGHT_POINTS
        else:
            iq.iq -= self.WRONG_PENALTY
        iq.save()

        data_to_send = {"user_is_correct": user_is_correct, "right_answer": right_answer.text,
                        "answer_sent": answer_sent.text}
        actual_question.delete()
        return Response(status=status.HTTP_200_OK, data=data_to_send)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def options_asked(self, request, pk):
        category = get_object_or_404(self.queryset, pk=pk)
        actual_question = self.question_user_model.objects.filter(question__category=category, user=request.user).first()
        print(actual_question.options_asked)
        if actual_question is None:
            data_to_send = {"options_asked": False}
        else:
            data_to_send = {"options_asked": actual_question.options_asked}
        return Response(status=status.HTTP_200_OK, data=data_to_send)
