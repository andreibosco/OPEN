from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from OPEN.course.models import Course, Forum, UploadedFile


@login_required
def course(request, course_id, template_name):
    """
    Course Page
    """
    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        pass
    return render_to_response(template_name, context_instance=RequestContext(request, {'course': course}))

@login_required
def all_user_courses(request, template_name):
    """
    Display all courses for a user
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))
    
    #grades = Grade.objects.filter(user = user)
    #Grade is the relationship between a course and a student
    #course registration not done.
    courses = Course.objects.all()
    return render_to_response(template_name, context_instance=RequestContext(request, {'courses': courses}))

@login_required
def course_pdf_list(request, course_id, template_name):
    """
    Display list of pdfs against a course
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        course = None
    
    pdfs = UploadedFile.objects.filter(file_type = 'PDF')
 
    return render_to_response(template_name, context_instance=RequestContext(request, {'pdfs': pdfs, 'course': course}))

@login_required
def view_file(request, course_id, pdf_id, template_name):
    """
    Display pdf file 
    """
    pdf = UploadedFile.objects.get(id = pdf_id)
    name = pdf.uploads.name.split('/')[1]

    with open('%s%s' % (settings.MEDIA_ROOT, pdf.uploads)) as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=%s' % name
        return response
    pdf.closed

@login_required
def course_video_list(request, course_id, template_name):
    """
    Display list of videos against a course
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        course = None
    
    videos = UploadedFile.objects.filter(file_type = 'VID')
    return render_to_response(template_name, context_instance=RequestContext(request, {'videos': videos, 'course': course}))

@login_required
def view_video_file(request, course_id, video_id, template_name):
    vid = UploadedFile.objects.get(id = video_id)
    return render_to_response(template_name,  context_instance=RequestContext(request, {'vid': vid}))

@login_required
def course_forum_list(request, course_id, template_name):
    """
    Display list of forums against a course
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        course = None

    forums = Forum.objects.filter(course = course)
    return render_to_response(template_name, context_instance=RequestContext(request, {'forums': forums, 'course': course}))

