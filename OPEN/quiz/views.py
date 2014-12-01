from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

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

        return HttpResponseRedirect(reverse('quiz_result', args=[quiz.course.id]))

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
        quiz = Quiz.objects.get(id = '1')
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

    iterator = ['1','2','3','4','5']
    data = {
        'quiz': quiz,
        'mcquestion': mcquestion,
        'likert': likert,
        'openended': openended,
        'iterator': iterator,
        'score': score,
        'total_score': total_score,
    }
    return render_to_response(template_name, context_instance=RequestContext(request, data))

