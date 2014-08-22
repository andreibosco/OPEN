from django.conf.urls import patterns, url

from OPEN.course.views import all_user_courses, course, course_forum_list, course_pdf_list, course_video_list, view_file, view_video_file


urlpatterns = patterns('',

    url( r'^$', 
        all_user_courses,
        {'template_name': 'course/all_user_courses.html'},
        name = 'all_user_courses' ),
        
    url( r'^(?P<course_id>\d+)/$', 
        course,
        {'template_name': 'course/course.html'},
        name = 'course' ),

    url( r'^(?P<course_id>\d+)/pdf/$', 
        course_pdf_list,
        {'template_name': 'course/course_pdf_list.html'},
        name = 'course_pdf_list' ),

    url( r'^(?P<course_id>\d+)/pdf/(?P<pdf_id>\d+)/$', 
        view_file,
        {'template_name': 'course/view_file.html'},
        name = 'view_file' ),

    url( r'^(?P<course_id>\d+)/video/$', 
        course_video_list,
        {'template_name': 'course/course_video_list.html'},
        name = 'course_video_list' ),

    url( r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/$', 
        view_video_file,
        {'template_name': 'course/view_video_file.html'},
        name = 'view_video_file' ),

    url( r'^(?P<course_id>\d+)/forum/$', 
        course_forum_list,
        {'template_name': 'course/course_forum_list.html'},
        name = 'course_forum_list' ),
)


