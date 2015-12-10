# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from . import views

urlpatterns = [

    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        base_views.root_txt_files, name='root-txt-files'),

    # Rest API
    url(r'^api/', include(router.urls)),

    # Browsable API
    url(r'^api/auth-n/', include('rest_framework.urls', namespace='rest_framework')),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

    # pages/ landing pages
    url(r'^', include("auth_server.pages.urls", namespace="pages")),

    # accounts/ registration
    url(r'^accounts/', include(registration_urls)),

    # Your stuff: custom urls go here

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
