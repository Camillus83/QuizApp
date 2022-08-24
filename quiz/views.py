from django.shortcuts import render
from django.db.models import Q


from .models import Quiz
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = "quiz/quiz_list.html"
    context_object_name = "quiz_list"
    login_url = "account_login"


class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = "quiz/quiz_detail.html"
    context_object_name = "quiz"
    login_url = "account_login"


class SearchResultsListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = "quiz/search_results.html"
    context_object_name = "quiz_list"
    login_url = "account_login"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Quiz.objects.filter(
            Q(title__icontains=query) | Q(author__username__icontains=query)
        )


class MyQuizesListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = "quiz/my_quizes.html"
    context_object_name = "quiz_list"
    login_url = "account_login"

    def myquiz_queryset(self):
        query = self.request.GET.get("q")
        return Quiz.objects.filter(Q(author__username__icontains=query))


class QuizUpdateView(LoginRequiredMixin, UpdateView):
    model = Quiz
    fields = (
        "title",
        "short_description",
        "resolution_time",
        "number_of_questions",
        "author",
    )
    template_name = "quiz/quiz_edit.html"
    success_url = ""


class QuizDeleteView(LoginRequiredMixin, DeleteView):
    pass
