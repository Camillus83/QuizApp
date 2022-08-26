from django.urls import path, include
from .views import (
    QuizListView,
    QuizDetailView,
    QuizUpdateView,
    SearchResultsListView,
    MyQuizesListView,
    QuizQuestionsUpdateView,
    QuizDeleteView,
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
]
