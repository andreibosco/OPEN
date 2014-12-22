from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from OPEN.base.models import TimeStampAwareModel
from OPEN.course.models import Course, UploadedFile


class Quiz( TimeStampAwareModel ):
    """
    Quiz model
    """
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)    
    video = models.ForeignKey(UploadedFile)

    title = models.CharField(_('title'), max_length = 100)
    description = models.TextField(_('description'), null = True, blank = True)

    def __unicode__(self):
        return _("%s") % (self.title)

    class Meta:
        app_label = "quiz"
        verbose_name = "quiz"
        verbose_name_plural = "quizzes"


class Question( TimeStampAwareModel ):
    """
    Question model
    Parent for Multiple Choice, Likert Scale and Open Ended questions
    """
    quiz = models.ForeignKey(Quiz)

    content = models.CharField(_('content'), max_length = 1000)
    description = models.TextField(_('description'), null = True, blank = True)    

    def __unicode__(self):
        return _("Question for %s") % (self.quiz.title)

    class Meta:
        app_label = "quiz"
        verbose_name = "question"
        verbose_name_plural = "questions"


class Choice( TimeStampAwareModel ):
    """
    Choice model
    Choices for MCQuestions
    """
    content = models.CharField(_('content'), max_length = 100)

    def __unicode__(self):
        return _("%s") % (self.content)

    class Meta:
        app_label = "quiz"
        verbose_name = "choice"
        verbose_name_plural = "choices"


class MCQuestion( Question ):
    """
    MCQ model
    """
    choice = models.ManyToManyField(Choice)
    
    def __unicode__(self):
        return _("%s") % (self.content)

    class Meta:
        app_label = "quiz"
        verbose_name = "multiple choice question"
        verbose_name_plural = "multiple choice questions"


class MCQAnswer( TimeStampAwareModel ):
    """
    MCQuestion Answer model
    """
    question = models.ForeignKey(MCQuestion)
    correct = models.ForeignKey(Choice)

    def __unicode__(self):
        return _("%s_%s") % (self.question.content, self.question.quiz.video)

    class Meta:
        app_label = "quiz"
        verbose_name = "MCQ answer"
        verbose_name_plural = "MCQ answers"


class Likert( Question ):
    """
    Likert model
    """

    def __unicode__(self):
        return _("%s") % (self.content)

    class Meta:
        app_label = "quiz"
        verbose_name = "likert scale question"
        verbose_name_plural = "likert scale question"


class LikertAnswer( TimeStampAwareModel ):
    """
    Likert Answer model
    """
    SCALE_CHOICES = (
	    ('', ''),
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    question = models.ForeignKey(Likert)
    correct = models.CharField(max_length = 2,
                                 choices = SCALE_CHOICES,
                                 blank = True,
                                 null = True,
                                 default = '')

    def __unicode__(self):
        return _("%s, %s") % (self.question.content, self.question.quiz.video)

    class Meta:
        app_label = "quiz"
        verbose_name = "likert answer"
        verbose_name_plural = "likert answers"


class OpenEnded( Question ):
    """
    Open Ended model
    """

    def __unicode__(self):
        return _("%s") % (self.content)

    class Meta:
        app_label = "quiz"
        verbose_name = "open ended question"
        verbose_name_plural = "open ended questions"


class MCQuestionAttempt( TimeStampAwareModel ):
    """
    MCQuestion Attempt model
    """
    answer = models.ForeignKey(Choice)
    mcquestion = models.ForeignKey(MCQuestion)
    student = models.ForeignKey(User)
    
    correct = models.NullBooleanField(blank = True, null = True)
    no_of_attempt = models.PositiveIntegerField(default = 1)
    
    
    def __unicode__(self):
        return _("%s_%s_%s") % (self.student.username, self.mcquestion.quiz, self.no_of_attempt)

    class Meta:
        app_label = "quiz"
        verbose_name = "multiple choice question attempt"
        verbose_name_plural = "multiple choice question attempts"


class LikertAttempt( TimeStampAwareModel ):
    """
    Liket Attempt model
    """
    SCALE_CHOICES = (
	('', ''),
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),        
    )

    likert = models.ForeignKey(Likert)
    student = models.ForeignKey(User)

    correct = models.NullBooleanField(blank = True, null = True)
    no_of_attempt = models.PositiveIntegerField(default = 1)    
    scale = models.CharField(max_length = 2,
                                 choices = SCALE_CHOICES,
                                 blank = True,
                                 null = True,
                                 default = '')

    def __unicode__(self):
        return _("%s_%s_%s") % (self.student.username, self.likert.quiz, self.no_of_attempt)

    class Meta:
        app_label = "quiz"
        verbose_name = "likert scale attempt"
        verbose_name_plural = "likert scale attempts"


class OpenEndedAttempt( TimeStampAwareModel ):
    """
    Open Ended Attempt model
    """
    openended = models.ForeignKey(OpenEnded)
    student = models.ForeignKey(User)
    
    answer = models.TextField(_('answer'), null = True, blank = True)        
    no_of_attempt = models.PositiveIntegerField(default = 1)    
  
    def __unicode__(self):
        return _("%s_%s_%s") % (self.student.get_full_name(), self.openended.quiz, self.no_of_attempt)

    class Meta:
        app_label = "quiz"
        verbose_name = "open ended attempt"
        verbose_name_plural = "open ended attempts"
