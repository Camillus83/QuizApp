from uuid import UUID, uuid1, uuid4
from django.shortcuts import render
from django.db.models import Q
from django.views.generic.detail import SingleObjectMixin
from .forms import QuizQuestionsFormset, QuestionAnswerFormset
from .models import Quiz, Question, Answer, Attempt
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse


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

    def get_absolute_url_create(self):
        return reverse("quiz_create")

    def myquiz_queryset(self):
        query = self.request.GET.get("q")
        return Quiz.objects.filter(Q(author__username__icontains=query))


class MyAttemptsListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = "quiz/attempts_list.html"
    login_url = "account_login"
    ordering = ["-attempt_date"]
    paginate_by = 10

    def myattempts_queryset(self):
        query = self.request.GET.get("q")
        return Attempt.objects.filter(Q(user__username__icontains=query))


class QuizUpdateView(LoginRequiredMixin, UpdateView):
    model = Quiz
    template_name = "quiz/quiz_edit.html"
    context_object_name = "quiz"
    fields = ("title", "short_description", "resolution_time", "number_of_questions")

    def get_success_url(self):
        return reverse_lazy("my_quiz")


class QuizDeleteView(LoginRequiredMixin, DeleteView):
    model = Quiz
    template_name = "quiz/quiz_delete.html"
    context_object_name = "quiz"
    success_url = reverse_lazy("my_quiz")


class QuizQuestionsUpdateView(LoginRequiredMixin, SingleObjectMixin, FormView):

    model = Quiz
    template_name = "quiz/quiz_questions_edit.html"
    success_url = reverse_lazy("my_quiz")
    login_url = "account_login"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        return super().post(
            request, Quiz.id ** self.get_form_kwargs(), instance=self.object
        )

    def get_form(self, form_class=None):
        return QuizQuestionsFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("my_quiz")


class QuestionAnswerView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Question
    template_name = "quiz/question_answer_edit.html"
    login_url = "account_login"

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
        self.object = self.get_object(queryset=Question.objects.all())
        quizpk = self.object.quiz.pk
        return reverse_lazy("quiz_questions_edit", kwargs={"pk": quizpk})


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    template_name = "quiz/quiz_create.html"
    context_object_name = "quiz"
    fields = ("title", "short_description", "resolution_time", "number_of_questions")
    login_url = "account_login"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("my_quiz")


class QuizPlayView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = "quiz/quiz_play.html"
    context_object_name = "quiz"
    login_url = "account_login"


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions_QS = Question.objects.filter(quiz=quiz)
    questions = []
    for q in questions_QS:
        answers = []
        answers_QS = Answer.objects.filter(question=q)
        for a in answers_QS:
            answers.append(a.content)
        questions.append({str(q.content): answers})
    return JsonResponse(
        {
            "data": questions,
            "time": quiz.resolution_time,
        }
    )


def save_quiz_view(request, pk):
    questions = []
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = request.POST
        data_ = dict(data.lists())

        data_.pop("csrfmiddlewaretoken")

        for k in data_.keys():
            print("key:", k)
            question = Question.objects.get(content=k)
            questions.append(question)
        print(questions)
        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        max_score = Question.objects.filter(quiz=quiz).count()
        score = 0
        multiplier = 100 / max_score
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for answer in question_answers:
                    if a_selected == answer.content:
                        if answer.is_correct:
                            score += 1
                            correct_answer = answer.content
                    else:
                        if answer.is_correct:
                            correct_answer = answer.content
                results.append(
                    {
                        str(q): {
                            "correct_answer": correct_answer,
                            "answered": a_selected,
                        }
                    }
                )
            else:
                results.append({str(q): "not answered"})

        score_ = score * multiplier
        Attempt.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse(
                {"passed": True, "score": score_, "attempt_details": results}
            )
        if score_ < quiz.required_score_to_pass:
            return JsonResponse(
                {"passed": False, "score": score_, "attempt_details": results}
            )


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, "quiz/quiz.html", {"obj": quiz})
