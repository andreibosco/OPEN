from django.conf.urls import patterns, url

from OPEN.quiz.views import quiz


urlpatterns = patterns('',

     url( r'^(?P<quiz_id>\d+)/$', 
        quiz,
        {'template_name': 'quiz/quiz.html'},
        name = 'quiz' ),


)
