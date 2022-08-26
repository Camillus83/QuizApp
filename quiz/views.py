from django.shortcuts import render
from django.db.models import Q
from django.forms import inlineformset_factory
from django.views.generic.detail import SingleObjectMixin
from .forms import QuizQuestionsFormset, QuestionAnswerFormset, QuizForm
from .models import Quiz, Question
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

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
    template_name = "quiz/quiz_edit.html"
    context_object_name = "quiz"
    fields = ("title", "short_description")


class QuizDeleteView(LoginRequiredMixin, DeleteView):
    model = Quiz
    template_name = "quiz/quiz_delete.html"
    context_object_name = "quiz"
    success_url = reverse_lazy("my_quiz")


class QuizQuestionsUpdateView(SingleObjectMixin, FormView):

    model = Quiz
    template_name = "quiz/quiz_questions_edit.html"
    success_url = reverse_lazy("my_quiz")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return QuizQuestionsFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        """messages.add_message(self.request, message.SUCCESS, "changes were saved.")"""
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("my_quiz")


class QuestionAnswerView(SingleObjectMixin, FormView):
    model = Question
    template_name = "quiz/question_answer_edit.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Question.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Question.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return QuestionAnswerFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("my_quiz")
