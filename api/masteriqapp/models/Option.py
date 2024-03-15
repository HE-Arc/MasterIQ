from django.db import models
from masteriqapp.models.Question import Question


class Option(models.Model):
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)

    def __str__(self):
        right_or_wrong = "Right" if self.is_correct else "Wrong"
        return f"{right_or_wrong} : {self.text}"
