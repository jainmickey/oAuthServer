import hashlib
import urllib
import shortuuid

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

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
