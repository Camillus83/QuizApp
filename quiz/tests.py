from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Quiz, Question, Answer


class QuizTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.quizmaker = get_user_model().objects.create_user(
            username="quizmaker", email="quizmaker@email.com", password="testpass123"
        )

        cls.quiz = Quiz.objects.create(
            title="Python Quiz",
            author=cls.quizmaker,
            short_description="Very easy quiz",
            number_of_questions=5,
        )

        cls.question = Question.objects.create(
            quiz=cls.quiz,
            content="Is python a snake?",
        )

        cls.correctanswer = Answer.objects.create(
            question=cls.question,
            content="Yes",
            is_correct=True,
        )

        cls.wronganswer = Answer.objects.create(
            question=cls.question,
            content="No",
            is_correct=False,
        )

    def test_quiz_creation(self):
        self.assertEqual(f"{self.quiz.title}", "Python Quiz")
        self.assertEqual(f"{self.quiz.short_description}", "Very easy quiz")
        # self.assertEqual(f"{self.quiz.author}", self.quizmaker) HOW TO FIX THAT??? !!!!!!!!!
        self.assertEqual(self.quiz.number_of_questions, 5)

    def test_quiz_list_view(self):
        response = self.client.get(reverse("quiz_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Quiz")
        self.assertTemplateUsed(response, "quiz/quiz_list.html")

    def test_quiz_detail_view(self):
        response = self.client.get(self.quiz.get_absolute_url())
        no_response = self.client.get("/quiz/123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, self.quiz.title)
        self.assertContains(response, self.quiz.author)
        self.assertTemplateUsed(response, "quiz/quiz_detail.html")
