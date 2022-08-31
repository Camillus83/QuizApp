from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
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
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"Quiz title: {self.title}"

    def get_answers(self):
        return self.quiz.question.answers_set.all()

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

    def get_absolute_url_answer_edit(self):
        return reverse("question_answer_edit")

    def get_absolute_url_create(self):
        return reverse("quiz_create")

    def get_absolute_url_play(self):
        return reverse("quiz_play", args=[str(self.id)])


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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.SmallIntegerField(default=1)
    has_passed = models.BooleanField(default=False)
    attempt_date = models.DateTimeField(auto_now_add=True)
