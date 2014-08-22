from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from OPEN.userprofile.forms import UserProfileForm
from OPEN.userprofile.views import index, registration

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OPEN.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/register/$', registration, {'template_name': 'registration/registration_form.html'}, name='registration_register'),

    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^comments/', include('django.contrib.comments.urls')),

    url( r'^$', 
        index,
        { 'template_name': 'index.html' },
        name = 'index' ),

    url(r'^profile/', include('OPEN.userprofile.urls')),

    url(r'^course/', include('OPEN.course.urls')),
    


)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

    url(r'^adminmedia/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.STATIC_ROOT + '/admin', 'show_indexes': True}),
)
