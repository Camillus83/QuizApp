from django.contrib import admin
from .models import Quiz, Question, Answer

# Register your models here.
class QuestionInLine(admin.TabularInline):
    model = Question


class AnswerInLine(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInLine,
    ]
    list_display = ("quiz", "content")


class QuizAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInLine,
    ]
    list_display = ("title", "short_description", "number_of_questions")


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
