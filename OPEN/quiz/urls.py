from django.conf.urls import patterns, url

from OPEN.quiz.views import quiz, quiz_result


urlpatterns = patterns('',

     url( r'^(?P<quiz_id>\d+)/$', 
        quiz,
        {'template_name': 'quiz/quiz.html'},
        name = 'quiz' ),

    url( r'^(?P<quiz_id>\d+)/result/$',
        quiz_result,
        {'template_name': 'quiz/quiz_result.html'},
        name = 'quiz_result' ),

)
