from dataclasses import fields
from django.forms.models import inlineformset_factory
from django import forms
from .models import Quiz, Question, Answer


QuizQuestionsFormset = inlineformset_factory(
    Quiz, Question, fields=("content",), extra=1, can_delete=True
)

QuestionAnswerFormset = inlineformset_factory(
    Question, Answer, fields=("content", "is_correct"), extra=4, can_delete=True
)


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            "title",
            "short_description",
            "resolution_time",
            "number_of_questions",
        ]
