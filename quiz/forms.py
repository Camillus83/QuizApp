from dataclasses import fields
from django.forms.models import inlineformset_factory
from django import forms
from .models import Quiz, Question

QuizQuestionsFormset = inlineformset_factory(Quiz, Question, fields=("content",))


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            "title",
            "short_description",
        ]
