from django.urls import path, include
from .views import (
    QuizListView,
    QuizDetailView,
    QuizUpdateView,
    SearchResultsListView,
    MyQuizesListView,
    MyAttemptsListView,
    QuizQuestionsUpdateView,
    QuizDeleteView,
    QuestionAnswerView,
    QuizCreateView,
    quiz_data_view,
    quiz_view,
    save_quiz_view,
)

urlpatterns = [
    path("", QuizListView.as_view(), name="quiz_list"),  # HomePage, all Quizes.
    path(
        "myquiz/", MyQuizesListView.as_view(), name="my_quiz"
    ),  # List of Quizes where author is currently logged in user.
    path(
        "myattempts/", MyAttemptsListView.as_view(), name="my_attempts"
    ),  # List of Attempts where taker is currenty logged in user.
    path(
        "search/", SearchResultsListView.as_view(), name="search_results"
    ),  # List of Quizes where Author or Title contains keyword
    path(
        "<uuid:pk>", QuizDetailView.as_view(), name="quiz_detail"
    ),  # Detail of chosen Quiz, is shows the title, short description, author, resolution time and amount of questions.
    # Quiz Edit Views
    path(
        "edit/questions/<uuid:pk>/",
        QuizQuestionsUpdateView.as_view(),  # View with all questions related to Quiz, on this view author can add/modify questions.
        name="quiz_questions_edit",
    ),
    path(
        "edit/<uuid:pk>/", QuizUpdateView.as_view(), name="quiz_edit"
    ),  # View where author can change Title/Short Description/Resolution Time/Number of questions of Quiz.
    path(
        "delete/<uuid:pk>/", QuizDeleteView.as_view(), name="quiz_delete"
    ),  # View where author can delete quiz.
    path(
        "edit/answer/<uuid:pk>",
        QuestionAnswerView.as_view(),  # View where author can change Answers related to Question.
        name="question_answer_edit",
    ),
    path(
        "new/", QuizCreateView.as_view(), name="quiz_create"
    ),  # View where author can create a new Quiz.
    # Quiz Logic Views
    path("play/<uuid:pk>", quiz_view, name="quiz_play"),
    path("play/<uuid:pk>/data", quiz_data_view, name="quiz_data"),
    path("play/<uuid:pk>/save", save_quiz_view, name="quiz_save"),
]
