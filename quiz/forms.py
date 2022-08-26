from dataclasses import fields
from django.forms.models import inlineformset_factory
from django import forms
from .models import Quiz, Question, Answer

QuizQuestionsFormset = inlineformset_factory(Quiz, Question, fields=("content",))
QuestionAnswerFormset = inlineformset_factory(Question, Answer, fields=("content",))


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            "title",
            "short_description",
        ]
