from django.conf.urls import patterns, url

from OPEN.account.views import username_available


urlpatterns = patterns('',

    url(r'^login$', 
	'django.contrib.auth.views.login', 
	{'template_name': 'registration/login.html'},
    ),

    url(r'^logout$', 
	'django.contrib.auth.views.logout', 
	{'next_page': '/accounts/login/'},
    ),

    url(r'^username/available/$',
       username_available,
       name = 'username_available'
    ),



)
