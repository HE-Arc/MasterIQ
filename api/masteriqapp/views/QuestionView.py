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
    iq_model = masteriq.get_model("IQ")
    queryset = category_model.objects.all()
    permission_classes = (IsAuthenticated,)

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
        request.session['options_asked'] = False
        serializer = QuestionSerializer(new_question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
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

        for option in datas['options']:
            option_serializer = OptionSerializer(data={"text": option, "is_correct": False, "question": 3})

            if option_serializer.is_valid():
                option_serializer.save()
            else:
                return Response(data={"field": "Option", "error": option_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        option_serializer = OptionSerializer(
            data={"text": datas['answer'], "is_correct": True, "question": question.id})
        if option_serializer.is_valid():
            question = option_serializer.save()
        else:
            return Response(data={"field": "Answer", "error": option_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(question_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def options(self, request):
        if not 'question' in request.session:
            return Response(status=449, data={"error": "No question being answered at the moment"})
        question_id = request.session['question']
        request.session['options_asked'] = True
        question = self.question_model.objects.get(pk=question_id)
        data_to_send = {'question_id': question.id, 'number_of_options': len(question.options.all()), 'options': {}}
        for option in question.options.all():
            data_to_send['options'][option.id] = option.text
        return Response(status=status.HTTP_200_OK, data=data_to_send)

    @action(detail=False, methods=["POST"], url_path="answer_text")
    def answer_text(self, request):
        if not 'answer' in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No answer given"})
        if not 'question' in request.session or not 'options_asked' in request.session:
            return Response(status=449, data={"error": "No question being answered at the moment"})
        if request.session['options_asked']:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Options already asked, you can only "
                                                                               "answer with options"})
        question = self.question_model.objects.get(pk=request.session['question'])
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
        del request.session['question']
        del request.session['options_asked']
        return Response(status=status.HTTP_200_OK, data=data_to_send)

    @action(detail=False, methods=["POST"], url_path="answer_option")
    def answer_options(self, request):
        if not 'answer' in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No answer given"})
        if not 'question' in request.session or not 'options_asked' in request.session:
            return Response(status=449, data={"error": "No question being answered at the moment"})
        if not request.session['options_asked']:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "Options already asked, you can only "
                                           "answer with options"})
        question = self.question_model.objects.get(pk=request.session['question'])
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
        del request.session['question']
        del request.session['options_asked']
        return Response(status=status.HTTP_200_OK, data=data_to_send)

    @action(detail=False, methods=["GET"])
    def options_asked(self, request):
        if not 'question' in request.session or not 'options_asked' in request.session:
            data_to_send = {"options_asked": False}
        else:
            data_to_send = {"options_asked": request.session['options_asked']}
        return Response(status=status.HTTP_200_OK, data=data_to_send)
