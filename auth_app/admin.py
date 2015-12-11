# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib import admin

from . import models


# ModelAdmins
# ----------------------------------------------------------------------------
@admin.register(models.App,
                models.Grant,
                models.AccessToken,
                models.Submission)
class UserApplication(admin.ModelAdmin):
    pass
