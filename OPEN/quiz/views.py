import xlwt

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from OPEN.course.models import UploadedFile
from OPEN.quiz.models import Choice, Likert, LikertAttempt, LikertAnswer, MCQuestion, MCQAnswer, MCQuestionAttempt, OpenEnded, OpenEndedAttempt, Quiz


@login_required
def quiz(request, quiz_id, template_name):
    """
    Attempt Quiz
    """
    try:
        quiz = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))        

    if request.method == "POST":
        flag = False
        for key, value in request.POST.iteritems():
            try:
                q_type = key.split('_')[0]
                q_id = key.split('_')[1]
            except:
                q_type = None
                q_id = None

            if q_type == 'mcquestion':
                try:
                    mcquestion = MCQuestion.objects.get(id = q_id)
                except MCQuestion.DoesNotExist:
                    mcquestion = None

                try:
                    answer = Choice.objects.get(content = value)
                except Choice.DoesNotExist:
                    answer = None

                try:
                    correct_answer = MCQAnswer.objects.get(question = mcquestion)
                except MCQAnswer.DoesNotExist:
                    correct_answer = None
                if correct_answer:
                    flag = True

                no_of_attempt = MCQuestionAttempt.objects.filter(mcquestion = mcquestion, student = request.user).aggregate(Max('no_of_attempt'))
                
                attempt = MCQuestionAttempt.objects.create(mcquestion = mcquestion, 
                                    student = request.user, answer = answer)
                
                if no_of_attempt['no_of_attempt__max']:
                    attempt.no_of_attempt = no_of_attempt['no_of_attempt__max'] + 1
                if correct_answer and answer == correct_answer.correct:
                    attempt.correct = True
                elif correct_answer and answer != correct_answer.correct:
                    attempt.correct = False
                attempt.save()

            elif q_type == 'likert':
                try:
                    likert = Likert.objects.get(id = q_id)
                except Likert.DoesNotExist:
                    likert = None

                try:
                    correct_answer = LikertAnswer.objects.get(question = likert)
                except LikertAnswer.DoesNotExist:
                    correct_answer = None
                if correct_answer:
                    flag = True

                no_of_attempt = LikertAttempt.objects.filter(likert = likert, student = request.user).aggregate(Max('no_of_attempt'))                

                attempt = LikertAttempt.objects.create(likert = likert, 
                                    student = request.user, scale = value)

                if no_of_attempt['no_of_attempt__max']:
                    attempt.no_of_attempt = no_of_attempt['no_of_attempt__max'] + 1
                if correct_answer and value == correct_answer.correct:
                    attempt.correct = True
                elif correct_answer and value != correct_answer.correct:
                    attempt.correct = False
                attempt.save()
            
            elif q_type == 'openended':
                try:
                    openended = OpenEnded.objects.get(id = q_id)
                except OpenEnded.DoesNotExist:
                    openended = None

                if value:
                    no_of_attempt = OpenEndedAttempt.objects.filter(openended = openended, student = request.user).aggregate(Max('no_of_attempt'))                

                    attempt = OpenEndedAttempt.objects.create(openended = openended, 
                                       student = request.user, answer = value)
                    
                    if no_of_attempt['no_of_attempt__max']:
                        attempt.no_of_attempt = no_of_attempt['no_of_attempt__max'] + 1
                    attempt.save()
        if flag and request.user.get_profile().feedback:
            return HttpResponseRedirect(reverse('quiz_result', args=[quiz.id]))
        else:
            return HttpResponseRedirect(reverse('course_quiz_list', args=[quiz.course.id]))

    else:
        mcquestions = MCQuestion.objects.filter(quiz = quiz)
        likert = Likert.objects.filter(quiz = quiz)
        openended = OpenEnded.objects.filter(quiz = quiz)

        data = {
            'quiz': quiz,
            'mcquestions': mcquestions,
            'likert': likert,
            'openended': openended,
        }
        return render_to_response(template_name, context_instance=RequestContext(request, data))

@login_required
def quiz_result(request, quiz_id, template_name):
    """
    Quiz Summary
    """
    try:
        quiz = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

    mcquestion_attempt = MCQuestionAttempt.objects.filter(mcquestion__quiz = quiz, student = request.user).aggregate(Max('no_of_attempt'))
    likert_attempt = LikertAttempt.objects.filter(likert__quiz = quiz, student = request.user).aggregate(Max('no_of_attempt'))
    openended_attempt = OpenEndedAttempt.objects.filter(openended__quiz = quiz, student = request.user).aggregate(Max('no_of_attempt'))

    no_of_attempt = max([mcquestion_attempt['no_of_attempt__max'], likert_attempt['no_of_attempt__max'], openended_attempt['no_of_attempt__max']])

    mcquestion = MCQuestionAttempt.objects.filter(mcquestion__quiz = quiz, student = request.user, no_of_attempt = no_of_attempt)
    likert = LikertAttempt.objects.filter(likert__quiz = quiz, student = request.user, no_of_attempt = no_of_attempt)
    openended = OpenEndedAttempt.objects.filter(openended__quiz = quiz, student = request.user, no_of_attempt = no_of_attempt)

    score = 0
    total_score = 0

    for mcq in mcquestion:
        if mcq.correct:
            score = score + 1
        total_score = total_score + 1

    for l in likert:
        if l.correct:
            score = score + 1
        total_score = total_score + 1


    mcq_count = MCQuestionAttempt.objects.filter(student = request.user).values('mcquestion__quiz').distinct().count()
    likert_count = LikertAttempt.objects.filter(student = request.user).values('likert__quiz').distinct().count()

    total = mcq_count + likert_count
    if total > 0 and total <= 2:
        top = 50
    elif total > 2 and total <= 10:
        top = 75
    elif total > 10:
        top = 90

    iterator = ['1','2','3','4','5']

    data = {
        'quiz': quiz,
        'mcquestion': mcquestion,
        'likert': likert,
        'openended': openended,
        'iterator': iterator,
        'top': top,
        'score': score,
        'total_score': total_score,
    }
    return render_to_response(template_name, context_instance=RequestContext(request, data))

def get_data(request):
    """
    Create an excel file with Questions and average score
    """
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="open.xls"'
    workbook = xlwt.Workbook()
    videos = UploadedFile.objects.filter(file_type='VID')
    for video in videos:
        mcquestions = MCQuestionAttempt.objects.filter(mcquestion__quiz__video = video)
        likert = LikertAttempt.objects.filter(likert__quiz__video = video)
        workbook = create_sheet(workbook, mcquestions, likert, video.title)
    if not videos:
        sheet = workbook.add_sheet("Empty")
        sheet.write(0, 0, 'No data available')
    workbook.save(response)
    return response

def create_sheet(workbook, mcqs, likert, video_title):
    """
    Create a excel sheet for Checklist and GRS
    """
    checklist = workbook.add_sheet(video_title)
    style = xlwt.easyxf('font: bold 1')
    checklist.write(0,0, 'Checklist (0 = No, 1 = Yes)', style)
    checklist.write(0,1, 'Score', style)
    checklist.write(0,2, 'No. of Raters', style)

    i = 1
    seen = []
    for question in mcqs:
        if question.mcquestion.id not in seen:
            attempts = mcqs
            checklist.write(i, 0, question.mcquestion.content)
            yes_count = 0
            no_count = 0
            for attempt in attempts:
                if attempt.mcquestion.id == question.mcquestion.id:
                    if attempt.answer.content == 'Yes':
                        yes_count = yes_count + 1
                    elif attempt.answer.content == 'No':
                        no_count = no_count + 1
            if yes_count > no_count:
                checklist.write(i, 1, 1)
            elif yes_count < no_count:
                checklist.write(i, 1, 0)
            else:
                checklist.write(i, 1, 'equal')
            checklist.write(i, 2, yes_count + no_count)
            i = i + 1
            seen.append(question.mcquestion.id)

    i = i + 1
    checklist.write(i,0, 'GRS (score of 1 to 5)', style)
    checklist.write(i,1, 'Score', style)
    checklist.write(i,2, 'No. of Raters', style)

    i = i + 1
    seen = []
    attempt = []
    for question in likert:
        if question.likert.id not in seen:
            attempts = likert
            checklist.write(i, 0, question.likert.content)
            zero = 0
            one = 0
            two = 0
            three = 0
            four = 0
            five = 0
            for attempt in attempts:
                if question.likert.id == attempt.likert.id:
                    if attempt.scale == '0':
                        zero = zero + 1
                    elif attempt.scale == '1':
                        one = one + 1
                    elif attempt.scale == '2':
                        two = two + 1
                    elif attempt.scale == '3':
                        three = three + 1
                    elif attempt.scale == '4':
                        four = four + 1
                    elif attempt.scale == '5':
                        five = five + 1

            d = {'0': zero, '1': one, '2': two, '3': three, '4': four, '5': five}
            maxx = max(d.values())
            keys = [x + ' ' for x,y in d.items() if y ==maxx]
            checklist.write(i, 1, keys)
            checklist.write(i, 2, sum(d.values()))

            i = i + 1
            seen.append(question.likert.id)
    return workbook

def user_attempt(request):
    """
    Create an excel file with Participant Attempts
    """
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="attempts.xls"'
    workbook = xlwt.Workbook()
    users = User.objects.all()
    for user in users:
        mcquestions = MCQuestionAttempt.objects.filter(student = user).order_by('mcquestion__quiz__video')
        workbook = create_attempt_sheet(workbook, user, mcquestions, likert=None)

    workbook.save(response)
    return response

def create_attempt_sheet(workbook, user, mcquestions, likert):
    """
    Create an excel sheet for Participant attempt
    """
    checklist = workbook.add_sheet(user.username)
    style = xlwt.easyxf('font: bold 1')
    i = 0
    video = None
    for mcquestion in mcquestions:
        if video == mcquestion.mcquestion.quiz.video:
            checklist.write(i,j, mcquestion.mcquestion.content)
            if mcquestion.answer.content:
                checklist.write(i,j+1, 1)
                answer = 1
            else:
                checklist.write(i, j+1, 0)
                answer = 0
            if mcquestion.correct:
                checklist.write(i,j+2, answer)
                checklist.write(i,j+3, 0)
            else:
                if mcquestion.answer.content:
                    checklist.write(i,j+2, 0)
                else:
                    checklist.write(i,j+2, 1)
                checklist.write(i,j+3, 1)

            i += 1
        else:
            j = 0
            video = mcquestion.mcquestion.quiz.video
            checklist.write(i,j, video.title, style)
            checklist.write(i,j+1, "Date: " + str(mcquestion.date_added.strftime('%B %d ')), style)
            checklist.write(i,j+3, "Input", style)
            checklist.write(i,j+4, "Answer", style)
            checklist.write(i,j+5, "Difference", style)
            checklist.write(i+1,j+2, "Checklist (0 = No, 1 = Yes)", style)
            i += 2
            j = 2
            checklist.write(i,j, mcquestion.mcquestion.content)
            if mcquestion.answer.content:
                checklist.write(i,j+1, 1)
                answer = 1
            else:
                checklist.write(i, j+1, 0)
                answer = 0
            if mcquestion.correct:
                checklist.write(i,j+2, answer)
                checklist.write(i,j+3, 0)
            else:
                if mcquestion.answer.content:
                    checklist.write(i,j+2, 0)
                else:
                    checklist.write(i,j+2, 1)
                checklist.write(i,j+3, 1)
            i += 1
    return workbook