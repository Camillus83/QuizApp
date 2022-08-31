from django.urls import path, include
from .views import (
    QuizListView,
    QuizDetailView,
    QuizUpdateView,
    SearchResultsListView,
    MyQuizesListView,
    QuizQuestionsUpdateView,
    QuizDeleteView,
    QuestionAnswerView,
    QuizCreateView,
    QuizPlayView,
    quiz_data_view,
    quiz_view,
    save_quiz_view,
)

urlpatterns = [
    path("", QuizListView.as_view(), name="quiz_list"),
    path("myquiz/", MyQuizesListView.as_view(), name="my_quiz"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path("<uuid:pk>", QuizDetailView.as_view(), name="quiz_detail"),
    path(
        "edit/questions/<uuid:pk>/",
        QuizQuestionsUpdateView.as_view(),
        name="quiz_questions_edit",
    ),
    path("edit/<uuid:pk>/", QuizUpdateView.as_view(), name="quiz_edit"),
    path("delete/<uuid:pk>/", QuizDeleteView.as_view(), name="quiz_delete"),
    path(
        "edit/answer/<uuid:pk>",
        QuestionAnswerView.as_view(),
        name="question_answer_edit",
    ),
    path("new/", QuizCreateView.as_view(), name="quiz_create"),
    path("play/<uuid:pk>", quiz_view, name="quiz_play"),
    path("play/<uuid:pk>/data", quiz_data_view, name="quiz_data"),
    path("play/<uuid:pk>/save", save_quiz_view, name="quiz_save"),
]
