from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from OPEN.base.models import TimeStampAwareModel

from django_countries.fields import CountryField
from PIL import Image
from registration.signals import user_registered
 

class UserProfile( TimeStampAwareModel ):
    """
    Profile model
    """
    user = models.ForeignKey(User)
    
    avatar = models.ImageField(_('profile pic'), upload_to = "images/", null = True, blank = True)
    address = models.CharField(_('address'), max_length = 50, null = True, blank = True)
    country = CountryField(_('country'), null = True, blank = True)
    city = models.CharField(_('city'), max_length = 30, null = True, blank = True)
    phone = models.CharField(_('phone number'), max_length = 20, null = True, blank = True)
    date_of_birth = models.DateField(_('date of birth'), null = True, blank = True)
    website = models.URLField(_('website'), null = True, blank = True)

    def __unicode__(self):
        return _("%s") % self.user.get_full_name()

    def is_authenticated(self):
        return self.user.is_authenticated()

    class Meta:
        app_label = "userprofile"
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"


def user_profile_callback(sender, user, request, **kwargs):
    profile = UserProfile(user = user)
    profile.save()
 
user_registered.connect(user_profile_callback)


