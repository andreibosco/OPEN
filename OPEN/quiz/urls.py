from django.conf.urls import patterns, url

from OPEN.quiz.views import get_data, instructor_attempt, likert_add, mcquestion_add, openended_add, quiz, quiz_add, quiz_result, user_attempt


urlpatterns = patterns('',

     url( r'^(?P<quiz_id>\d+)/$', 
        quiz,
        {'template_name': 'quiz/quiz.html'},
        name = 'quiz' ),

    url( r'^(?P<quiz_id>\d+)/attempt/$',
        instructor_attempt,
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

    url(r'^(?P<course_id>\d+)/add/$',
       quiz_add,
       {'template_name': 'quiz/quiz_add.html'},
       name = 'quiz_add' ),

    url(r'^(?P<quiz_id>\d+)/mcquestions/$',
       mcquestion_add,
       {'template_name': 'quiz/mcquestion_add.html'},
       name = 'mcquestion_add' ),

    url(r'^(?P<quiz_id>\d+)/likert/$',
       likert_add,
       {'template_name': 'quiz/likert_add.html'},
       name = 'likert_add' ),

    url(r'^(?P<quiz_id>\d+)/openended/$',
       openended_add,
       {'template_name': 'quiz/openended_add.html'},
       name = 'openended_add' ),
)
