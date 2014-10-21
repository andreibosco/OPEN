from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from OPEN.base.models import TimeStampAwareModel
from OPEN.institute.models import Institute

from django_countries.fields import CountryField


class Course( TimeStampAwareModel ):
    """
    Course model
    """
    institute = models.ForeignKey(Institute)    

    title = models.CharField(_('title'), max_length = 100)
    description = models.TextField(_('description'), null = True, blank = True)
    code = models.CharField(_('course code'), max_length = 30)
    start_date = models.DateTimeField(_('start date'), blank=True, null=True)
    end_date = models.DateTimeField(_('end date'), blank=True, null=True)

    def __unicode__(self):
        return _("%s") % (self.title)


    class Meta:
        app_label = "course"
        verbose_name = "course"
        verbose_name_plural = "courses"


class Grade( TimeStampAwareModel ):
    """
    Grade model
    """
    GRADE_CHOICES = (
	('', ''),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    )

    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    
    grade = models.CharField(max_length = 2,
                                 choices = GRADE_CHOICES,
                                 blank = True,
                                 null = True,
                                 default = '')

    def __unicode__(self):
        return _("%s_%s") % (self.user, self.course)


    class Meta:
        app_label = "course"
        verbose_name = "grade"
        verbose_name_plural = "grades"


class UploadedFile( TimeStampAwareModel ):
    """
    Uploaded Files (Video and PDF) model
    """
    FILE_CHOICES = (
        ('', ''),
        ('PDF', 'PDF'),
        ('VID', 'Video'),
            
    )
    
    uploader = models.ForeignKey(User)
    course = models.ForeignKey(Course)

    uploads = models.FileField(blank=True, upload_to='uploaded_files')
    file_type = models.CharField(max_length = 3, 
                                    choices = FILE_CHOICES,
                                    default = '')
    title = models.CharField(_('title'), max_length = 100)
    description = models.TextField(_('description'), null = True, blank = True)

    def __unicode__(self):
        return _("%s") % (self.title)

    class Meta:
        app_label = _("course")
        verbose_name = _("uploaded file")
        verbose_name_plural = _("uploaded files")


class Forum( TimeStampAwareModel ):
    """
    Forums models
    """
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    uploads = models.ForeignKey(UploadedFile)
    
    title = models.CharField(_('title'), max_length = 300)

    def __unicode__(self):
        return _("%s") % (self.title)

    class Meta:
        app_label = _("course")
        verbose_name = _("forum")
        verbose_name_plural = _("forums")
