from django.urls import path, include
from .views import QuizListView, QuizDetailView

urlpatterns = [
    path("", QuizListView.as_view(), name="quiz_list"),
    path("<uuid:pk>", QuizDetailView.as_view(), name="quiz_detail"),
]
