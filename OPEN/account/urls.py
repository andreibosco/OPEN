from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'^login$', 
	'django.contrib.auth.views.login', 
	{'template_name': 'registration/login.html'},
    ),

    url(r'^logout$', 
	'django.contrib.auth.views.logout', 
	{'next_page': '/accounts/login/'},
    ),

)
