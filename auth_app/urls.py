# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create_app$', views.createApplication,
        name='create_app'),
    url(r'^get_auth_code$', views.getAuthorizationCode,
        name='get_auth_code'),
    url(r'^get_access_token$', views.getAccessToken,
        name='get_access_token'),
    url(r'^submit_resume$', views.submitResume,
        name='submit_resume'),

]
