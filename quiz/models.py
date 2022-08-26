from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500)
    resolution_time = models.PositiveIntegerField(
        help_text="Quiz Duration in minutes", default=1
    )
    number_of_questions = models.PositiveIntegerField(default=1)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("quiz_detail", args=[str(self.id)])

    def get_absolute_url_edit(self):
        return reverse("quiz_edit", args=[str(self.id)])

    def get_absolute_url_questions_edit(self):
        return reverse("quiz_questions_edit", args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse("quiz_delete", args=[str(self.id)])

    def get_absolute_url_my_quizes(self):
        return reverse("my_quiz")


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    content = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.content


class Answer(models.Model):
    content = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def is_that_correct_answer(self):
        return self.is_correct


class Attempt(models.Model):
    pass
