from django.conf.urls import patterns, url

from OPEN.quiz.views import get_data, quiz, quiz_result, user_attempt


urlpatterns = patterns('',

     url( r'^(?P<quiz_id>\d+)/$', 
        quiz,
        {'template_name': 'quiz/quiz.html'},
        name = 'quiz' ),

    url( r'^(?P<quiz_id>\d+)/result/$',
        quiz_result,
        {'template_name': 'quiz/quiz_result.html'},
        name = 'quiz_result' ),

    url( r'^get_data/$',
        get_data,
        name = 'get_data' ),

    url( r'^user_attempt/$',
        user_attempt,
        name = 'user_attempt' ),

)
