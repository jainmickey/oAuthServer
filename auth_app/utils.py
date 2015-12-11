import hashlib
import urllib
import shortuuid
from multiprocessing.dummy import Pool

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from django_sites import get_current

current_site = get_current()
pool = Pool(processes=2)

CLIENT_PARAMS_SPACE = "0123456789abcdefghijk" + \
                      "lmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

Errors = {"invalid_client": [_("Missing Access Key"),
                             _("Invalid Access Key")],
          "invalid_request": [_("Missing Redirect Url"),
                              _("Invalid Redirect Url"),
                              _("Missing Authorization Code"),
                              _("Invalid Authorization Code"),
                              _("Missing Secret Key"),
                              _("Invalid Secret Key"),
                              _("Missing Access Token"),
                              _("Invalid Access Token")],
          "invalid_data": [_("Either Access Key or Redirect Url is Invalid")]}


def redirect_util(url, params):
    redirect_url = "%s?%s" % (url, urllib.urlencode(params))
    return HttpResponseRedirect(redirect_url)


def generate_token():
    """
    Generate a hash that can be used as an application secret
    """
    hash = hashlib.sha1(shortuuid.uuid())
    hash.update(settings.SECRET_KEY)
    return hash.hexdigest()


def send_mail_to_admin(sender, **kwargs):
    user = kwargs["instance"].user
    subject = _("%s has applied for a job through the API") % user.get_full_name()
    message = render_to_string("auth_app/application_message.txt",
                               {"resume": kwargs["instance"],
                                "site": current_site})
    pool.apply_async(send_mail, (subject, message, settings.DEFAULT_FROM_EMAIL,
                                 [manager[1] for manager in settings.MANAGERS]))


def send_mail_to_applicant(sender, **kwargs):
    user = kwargs["instance"].user
    subject = "Thank you for applying to %s" % current_site.name
    message = render_to_string("auth_app/application_confirmation.txt",
                               {"resume": kwargs["instance"],
                                "site": current_site})
    pool.apply_async(send_mail, (subject, message, settings.DEFAULT_FROM_EMAIL,
                                 [user.email]))
