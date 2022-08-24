from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView, DetailView

# Create your views here.
class QuizListView(ListView):
    model = Quiz
    template_name = "quiz/quiz_list.html"
    context_object_name = "quiz_list"


class QuizDetailView(DetailView):
    model = Quiz
    template_name = "quiz/quiz_detail.html"
    context_object_name = "quiz"
