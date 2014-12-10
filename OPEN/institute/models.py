from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from OPEN.base.models import TimeStampAwareModel

from django_countries.fields import CountryField


class Institute( TimeStampAwareModel ):
    """
    Institute model
    """
    user = models.ManyToManyField(User)

    title = models.CharField(_('title'), max_length = 100)
    description = models.TextField(_('description'), null = True, blank = True)
    country = CountryField(_('country'))

    def __unicode__(self):
        return _("%s") % (self.title)

    class Meta:
        app_label = "institute"
        verbose_name = "university"
        verbose_name_plural = "universities"


class Discipline( TimeStampAwareModel ):
    """
    Discipline model
    """
    institute = models.ManyToManyField(Institute)

    title = models.CharField(_('title'), max_length = 30)
    code = models.CharField(_('discipline code'), max_length = 30)
    description = models.TextField(_('description'), null = True, blank = True)

    def __unicode__(self):
        return _("%s") % (self.title)

    class Meta:
        verbose_name = "discipline"
        verbose_name_plural = "disciplines"


class SubDiscipline( TimeStampAwareModel ):
    """
    SubDiscipline model
    """
    institute = models.ForeignKey(Institute)
    discipline = models.ForeignKey(Discipline)

    title = models.CharField(_('title'), max_length = 30)
    description = models.TextField(_('description'), null = True, blank = True)
    code = models.CharField(_('subdiscipline code'), max_length = 30)

    def __unicode__(self):
        return _("%s") % (self.title)


    class Meta:
        verbose_name = "subdiscipline"
        verbose_name_plural = "subdisciplines"
        unique_together = (("institute", "discipline", "title"),)
