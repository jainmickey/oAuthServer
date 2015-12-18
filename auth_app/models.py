from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . import utils


class App(models.Model):
    """
    Application implementation

     @param user : User model foreign key
     @param name : Name of the application
     @param access_key : Generated public key for application
     @param secret_key : Generated private key for application
     @param redirect_uri : Application's callback url
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="user_apps",
                             blank=True, null=True)
    name = models.CharField(help_text=_('Application Name'), max_length=50,
                            blank=True, null=True)
    access_key = models.CharField(help_text=_('Access Key'), max_length=255,
                                  default=utils.generate_token)
    secret_key = models.CharField(help_text=_('Secret Key'), max_length=255,
                                  default=utils.generate_token)
    redirect_url = models.URLField(null=True,
                                   help_text=_("Your application's callback URL"))

    def __str__(self):
        return self.name


class Grant(models.Model):
    """
    Default grant implementation. A grant is a code that can be swapped for an
    access token. Grants have a limited lifetime as defined by
    :attr:`provider.constants.EXPIRE_CODE_DELTA` and outlined in
    :rfc:`4.1.2`

     @param user
     @param app : App model foreign key
     @param expires : datetime of expiry
     @param token : Generated private key for access
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="user_grants",
                             blank=True, null=True)
    app = models.ForeignKey(App, related_name="app_grant")
    token = models.CharField(max_length=255, default=utils.generate_token)
    expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token


class AccessToken(models.Model):
    """
    Default access token implementation. An access token is a time limited
    token to access a user's resources.
    Access tokens are outlined :rfc:`5`.

     @param user
     @param app : App model foreign key
     @param expires : datetime of expiry
     @param token : Generated private key for access
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="user_access_tokens",
                             blank=True, null=True)
    app = models.ForeignKey(App, related_name="app_access_token")
    token = models.CharField(max_length=255, default=utils.generate_token)
    expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token


class Submission(models.Model):
    """
    Submission of job application

     @param user
     @param resume : Uploaded Resume
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="user_resume_submission")
    resume = models.FileField(upload_to="resumes")

    def __str__(self):
        return '{}'.format(self.user.email)


post_save.connect(utils.send_mail_to_admin, sender=Submission)
post_save.connect(utils.send_mail_to_applicant, sender=Submission)
