import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils import simplejson

from OPEN.course.forms import AddForumForm
from OPEN.course.models import Course, Forum, Grade, UploadedFile
from OPEN.quiz.models import MCQuestionAttempt, LikertAttempt, OpenEndedAttempt, Quiz

from annoying.decorators import ajax_request
from threadedcomments.models import ThreadedComment


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
    
    grades = Grade.objects.filter(student = user, course__start_date__lte = datetime.datetime.now()).order_by('-date_added')

    return render_to_response(template_name, context_instance=RequestContext(request, {'grades': grades}))

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
        return HttpResponseRedirect(reverse('index'))        
    
    pdfs = UploadedFile.objects.filter(file_type = 'PDF', course = course.id)
 
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
        return HttpResponseRedirect(reverse('index'))                
    
    videos = UploadedFile.objects.filter(file_type = 'VID', course = course.id)
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

@login_required
def view_forum(request, course_id, forum_id, template_name):
    """
    Display the forum
    """
    try:
        forum = Forum.objects.get(id = forum_id)
    except Forum.DoesNotExist:
        forum = None

    return render_to_response(template_name, context_instance=RequestContext(request, {'forum': forum}))

@login_required
@ajax_request
def add_comment(request, course_id, forum_id):
    """
    Add a comment in the forum
    """
    if request.is_ajax() and request.POST.get('comment'):
        if request.method == 'POST':
            try:
                user = User.objects.get(username = request.user.username)
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('registration_register'))
            comment = request.POST.get('comment')
            
            comment = ThreadedComment.objects.create(comment = comment, user_id = user.id, content_type_id = '22', site_id = '1', object_pk = forum_id, submit_date = datetime.datetime.now())
            
            date = comment.submit_date.strftime("%b. %d, %Y, %I:%M ")
            if comment.submit_date.strftime('%p') == 'AM':
                date = str(date) + 'a.m.'
            else:
                date = str(date) + 'p.m.'

            if user.get_profile().avatar.url:
                avatar = str(user.get_profile().avatar.url)
            else:
                avatar = settings.STATIC_URL + "img/blank-avatar-50x50.jpg"
          
            return HttpResponse(simplejson.dumps({"status": True, "name": user.get_full_name(), "avatar": avatar, "comment": comment.comment, "date": str(date)}), mimetype = 'application/json')
    return HttpResponse(simplejson.dumps({"status": False}))

@login_required
def available_course(request, template_name):
    """
    Display list of courses available to the user
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))
    
    user_courses = Grade.objects.filter(student = user).values('course')
    
    list_course_ids = [course['course'] for course in user_courses]
    courses = Course.objects.exclude(id__in=list_course_ids)
  
    return render_to_response(template_name, context_instance=RequestContext(request, {'courses': courses}))

@login_required
def course_quiz_list(request, course_id, template_name):
    """
    Display list of quizzes against a course
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))                

    mcq = MCQuestionAttempt.objects.filter(student = user).values_list('mcquestion__quiz__id')
    lik = LikertAttempt.objects.filter(student = user).values_list('likert__quiz__id')
    opended = OpenEndedAttempt.objects.filter(student = user).values_list('openended__quiz__id')

    q_ids = [i[0] for i in mcq] + [i[0] for i in lik] + [i[0] for i in opended]
    quizzes = Quiz.objects.filter(course = course.id).exclude(id__in = q_ids)
    return render_to_response(template_name, context_instance=RequestContext(request, {'quizzes': quizzes, 'course': course}))

@login_required
@ajax_request
def add_course(request):
    """
    User can add a course
    """
    if request.is_ajax() and request.POST.get('course_id'):
        if request.method == 'POST':
            try:
                user = User.objects.get(username = request.user.username)
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('registration_register'))

            course_id = request.POST.get('course_id')
            
            try:
                course = Course.objects.get(id = course_id)
            except Course.DoesNotExist:
                return HttpResponse(simplejson.dumps({"status": False}))

            grade = Grade.objects.create(student = user, course = course)
            return HttpResponse(simplejson.dumps({"status": True, "course_id": course.id}))
    return HttpResponse(simplejson.dumps({"status": False}))
        
@login_required
def add_forum(request, course_id, template_name):
    """
    Create a new forum
    """
    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        course = None

    if request.method == 'POST':
        form = AddForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit = False)
            forum.user = request.user
            forum.course = course
            forum.save()
            return render_to_response('course/view_forum.html', context_instance=RequestContext(request, {'forum': forum}))
        else:
            return render_to_response(template_name, context_instance=RequestContext(request, {'form': form, 'course': course, 'course_id': course_id}))
    else:
        form = AddForumForm()
        return render_to_response(template_name, context_instance=RequestContext(request, {'form': form, 'course': course, 'course_id': course_id}))