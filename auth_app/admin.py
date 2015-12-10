# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib import admin

from .models import (App, Grant, AccessToken)


# ModelAdmins
# ----------------------------------------------------------------------------
@admin.register(App, Grant, AccessToken)
class UserApplication(admin.ModelAdmin):
    pass
