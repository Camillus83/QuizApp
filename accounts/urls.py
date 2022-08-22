from django.urls import path, include
from .views import SignUpPageView

urlpatterns = [
    path("signup/", SignUpPageView.as_view(), name="signup"),
]
