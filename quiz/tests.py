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
            is_public=True,
            resolution_time=10,
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
        """ Second Quizmaker """
        cls.quizmaker_2 = get_user_model().objects.create_user(
            username="quizmaker2", email="quizmaker2@email.com", password="testpass123"
        )

        cls.quiz_2 = Quiz.objects.create(
            title="Ruby Quiz",
            author=cls.quizmaker_2,
            short_description="Very difficult quiz",
        )

        cls.question_q2 = Question.objects.create(
            quiz=cls.quiz_2,
            content="Is ruby dead?",
        )

        cls.correctanswer_q2 = Answer.objects.create(
            question=cls.question_q2,
            content="Yes",
            is_correct=False,
        )

        cls.wronganswer_q2 = Answer.objects.create(
            question=cls.question_q2,
            content="No",
            is_correct=True,
        )

    # def test_check_user(self):
    #     self.assertTrue

    def test_quiz_creation(self):
        "Testing data"
        self.assertEqual(f"{self.quiz.title}", "Python Quiz")
        self.assertEqual(f"{self.quiz.short_description}", "Very easy quiz")
        self.assertEqual(f"{self.question.content}", "Is python a snake?")
        self.assertEqual(f"{self.correctanswer.content}", "Yes")
        self.assertEqual(f"{self.wronganswer.content}", "No")
        self.assertTrue(self.correctanswer.is_correct)
        self.assertFalse(self.wronganswer.is_correct)
        self.assertEqual(self.quiz.author, self.quizmaker)
        self.assertEqual(self.quiz.resolution_time, 10)
        self.assertEqual(self.quiz.is_public, True)
        "Testing relations between objects"
        self.assertEqual(self.question.quiz, self.quiz)
        self.assertEqual(self.correctanswer.question, self.question)
        self.assertEqual(self.wronganswer.question, self.question)
        self.assertEqual(self.correctanswer.question.quiz, self.quiz)
        self.assertEqual(self.wronganswer.question.quiz, self.quiz)

    """List View Tests"""

    def test_quiz_list_view_for_logged_in_user(self):

        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(reverse("quiz_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/quiz_list.html")
        self.assertContains(response, self.quiz.title)
        self.assertContains(response, self.quiz.short_description)
        self.assertNotContains(response, self.quiz_2.title)
        self.assertNotContains(response, self.quiz_2.short_description)

    def test_quiz_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse("quiz_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=/quiz/" % (reverse("account_login")))
        response = self.client.get("%s?next=/quiz/" % (reverse("account_login")))
        self.assertContains(response, "Login")

    """
    Detail View Tests"""

    def test_quiz_detail_view_for_logged_in_user(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(self.quiz.get_absolute_url())
        no_response = self.client.get("/quiz/123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, "quiz/quiz_detail.html")

        self.assertContains(response, self.quiz.title)
        self.assertContains(response, self.quiz.author)
        self.assertContains(response, self.question.content)
        self.assertContains(response, self.correctanswer.content)
        self.assertContains(response, self.wronganswer.content)

        self.assertNotContains(response, self.quiz_2.title)
        self.assertNotContains(response, self.question_q2.content)

    def test_quiz_detail_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.quiz.get_absolute_url())
        no_response = self.client.get("/quiz/123")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(no_response.status_code, 404)
        self.assertRedirects(
            response, "%s?next=/quiz/%s" % (reverse("account_login"), self.quiz.pk)
        )
        response = self.client.get(
            "%s?next=/quiz/%s" % (reverse("account_login"), self.quiz.pk)
        )
        self.assertContains(response, "Login")

    def test_my_quizzes_for_logged_in_user(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(self.quiz.get_absolute_url_my_quizes())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/my_quizes.html")

        self.assertContains(response, self.quiz.title)
        self.assertContains(response, self.quiz.author)
        self.assertContains(response, self.quiz.short_description)
        self.assertContains(response, self.quiz.resolution_time)

        self.assertNotContains(response, self.quiz_2.title)
        self.assertNotContains(response, self.quiz_2.author)
        self.assertNotContains(response, self.quiz_2.short_description)

    def test_edit_quiz_for_logged_in_author(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(self.quiz.get_absolute_url_edit())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/quiz_edit.html")

        self.assertContains(response, self.quiz.title)
        self.assertContains(response, self.quiz.short_description)
        self.assertContains(response, self.quiz.resolution_time)

    """FIX ITTTTTTTTTTTT!"""

    def test_edit_quiz_for_user_who_isnt_author(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(self.quiz_2.get_absolute_url_edit())
        self.assertEqual(response.status_code, 403)

    def test_edit_quiz_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.quiz.get_absolute_url_edit())
        no_response = self.client.get("/quiz/123")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(no_response.status_code, 404)
        self.assertRedirects(
            response,
            "%s?next=/quiz/edit/%s/" % (reverse("account_login"), self.quiz.pk),
        )
        response = self.client.get(
            "%s?next=/quiz/edit/%s/" % (reverse("account_login"), self.quiz.pk)
        )
        self.assertContains(response, "Login")

    """ QUESTIONS EDIT """

    def test_edit_quiz_questions_for_logged_in_author(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(self.quiz.get_absolute_url_questions_edit())
        no_response = self.client.get("/quiz/123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed("quiz_questions_edit.html")
        self.assertContains(response, self.question)
        self.assertNotContains(response, self.question_q2)

    def test_edit_quiz_questions_for_user_who_isnt_author(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(self.quiz_2.get_absolute_url_questions_edit())
        self.assertEqual(response.status_code, 403)

    def test_edit_quiz_questions_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.quiz.get_absolute_url_edit())
        no_response = self.client.get("/quiz/123")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(no_response.status_code, 404)
        self.assertRedirects(
            response,
            "%s?next=/quiz/edit/%s/" % (reverse("account_login"), self.quiz.pk),
        )
        response = self.client.get(
            "%s?next=/quiz/%s/" % (reverse("account_login"), self.quiz.pk)
        )
        self.assertContains(response, "Login")

    """  ANSWERS EDIT"""

    def test_edit_question_answers_for_logged_in_quiz_author(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get("/quiz/edit/answer/%s/" % self.question.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/question_answer_edit.html")
        self.assertContains(response, self.correctanswer)
        self.assertContains(response, self.wronganswer)

    def test_edit_question_answers_for_logged_in_user_who_isnt_author(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get("/quiz/edit/answer/%s/" % self.question_q2.pk)
        self.assertEqual(response.status_code, 403)

    def test_edit_question_answers_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.quiz.get_absolute_url_edit())
        no_response = self.client.get("/quiz/123")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(no_response.status_code, 404)
        self.assertRedirects(
            response,
            "%s?next=/quiz/edit/%s/" % (reverse("account_login"), self.quiz.pk),
        )
        response = self.client.get(
            "%s?next=/quiz/%s/" % (reverse("account_login"), self.quiz.pk)
        )
        self.assertContains(response, "Login")

    """ QUIZ DELETE"""

    def test_quiz_delete_for_logged_in_author(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(self.quiz.get_absolute_url_delete())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/quiz_delete.html")

    def test_quiz_delete_for_logged_in_another_user(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(self.quiz_2.get_absolute_url_delete())
        self.assertEqual(response.status_code, 403)

    def test_quiz_delete_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.quiz.get_absolute_url_delete())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "%s?next=/quiz/delete/%s/" % (reverse("account_login"), self.quiz.pk),
        )
        response = self.client.get(
            "%s?next=/quiz/delete/%s/" % (reverse("account_login"), self.quiz.pk)
        )
        self.assertContains(response, "Login")

    """ TAKE AN ATTEMPT """

    def test_quiz_attempt_for_logged_in_user(self):
        self.client.login(email="quizmaker@email.com", password="testpass123")
        response = self.client.get(self.quiz.get_absolute_url_play())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/quiz.html")

    def test_quiz_attempt_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.quiz.get_absolute_url_play())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "%s?next=/quiz/play/%s" % (reverse("account_login"), self.quiz.pk),
        )
        response = self.client.get(
            "%s?next=/quiz/play/%s" % (reverse("account_login"), self.quiz.pk)
        )
        self.assertContains(response, "Login")
