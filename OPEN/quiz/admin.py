from django.contrib import admin

from OPEN.quiz.models import Answer, Choice, Likert, MCQuestion, OpenEnded, Quiz, MCQuestionAttempt, LikertAttempt, OpenEndedAttempt 


class AnswerAdmin(admin.ModelAdmin):
    pass


class ChoiceAdmin(admin.ModelAdmin):
    pass


class LikertAdmin(admin.ModelAdmin):
    pass


class MCQuestionAdmin(admin.ModelAdmin):
    pass


class OpenEndedAdmin(admin.ModelAdmin):
    pass


class QuizAdmin(admin.ModelAdmin):
    pass


class MCQuestionAttemptAdmin(admin.ModelAdmin):
    pass


class LikertAttemptAdmin(admin.ModelAdmin):
    pass


class OpenEndedAttemptAdmin(admin.ModelAdmin):
    pass


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Likert, LikertAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(OpenEnded, OpenEndedAdmin)
admin.site.register(MCQuestionAttempt, MCQuestionAttemptAdmin)
admin.site.register(LikertAttempt, LikertAttemptAdmin)
admin.site.register(OpenEndedAttempt, OpenEndedAttemptAdmin)

