from dataclasses import fields
from django.forms.models import inlineformset_factory

from .models import Quiz, Question

QuizQuestionsFormset = inlineformset_factory(Quiz, Question, fields=("content",))
