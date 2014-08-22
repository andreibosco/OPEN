from django.conf.urls import patterns, url

from OPEN.userprofile.views import registration


urlpatterns = patterns('',

    url( r'^register$', 
        registration,
        {'template_name': 'registration/registration_form.html'},
        name = 'registration' ),

)


