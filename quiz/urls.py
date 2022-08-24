from django.urls import path, include
from .views import QuizListView, QuizDetailView, SearchResultsListView

urlpatterns = [
    path("", QuizListView.as_view(), name="quiz_list"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path("<uuid:pk>", QuizDetailView.as_view(), name="quiz_detail"),
]
