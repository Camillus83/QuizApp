from django.shortcuts import render
from django.db.models import Q
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


class SearchResultsListView(ListView):
    model = Quiz
    template_name = "quiz/search_results.html"
    context_object_name = "quiz_list"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Quiz.objects.filter(
            Q(title__icontains=query) | Q(author__username__icontains=query)
        )
