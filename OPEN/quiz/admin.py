from django.contrib import admin

from OPEN.quiz.models import Choice, Likert, LikertAnswer, MCQAnswer, MCQuestion, OpenEnded, Quiz, MCQuestionAttempt, LikertAttempt, OpenEndedAttempt


class ChoiceAdmin(admin.ModelAdmin):
    pass


class LikertAdmin(admin.ModelAdmin):
    pass


class LikertAnswerAdmin(admin.ModelAdmin):
    pass


class MCQAnswerAdmin(admin.ModelAdmin):
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


admin.site.register(MCQAnswer, MCQAnswerAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Likert, LikertAdmin)
admin.site.register(LikertAnswer, LikertAnswerAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(OpenEnded, OpenEndedAdmin)
admin.site.register(MCQuestionAttempt, MCQuestionAttemptAdmin)
admin.site.register(LikertAttempt, LikertAttemptAdmin)
admin.site.register(OpenEndedAttempt, OpenEndedAttemptAdmin)

