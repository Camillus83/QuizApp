from django.urls import path, include
from .views import SignUpPageView, GitHubView

urlpatterns = [
    path("signup/", SignUpPageView.as_view(), name="signup"),
    path("github/login", GitHubView.as_view(), name="github-view"),
]
