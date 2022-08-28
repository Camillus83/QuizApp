from django.contrib import admin
from .models import Quiz, Question, Answer, Attempt

# Register your models here.
class QuestionInLine(admin.TabularInline):
    model = Question


class AnswerInLine(admin.TabularInline):
    model = Answer


class AttemptInLine(admin.TabularInline):
    model = Attempt


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInLine,
    ]
    list_display = ("quiz", "content")


class QuizAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInLine,
    ]
    list_display = (
        "title",
        "short_description",
        "author",
        "number_of_questions",
        "resolution_time",
        "is_public",
    )


class AttemptAdmin(admin.ModelAdmin):
    inlines = [
        AttemptInLine,
    ]
    list_display = ("user", "quiz", "score", "has_passed", "attempt_date")


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(
    Attempt,
)
