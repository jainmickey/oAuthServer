"""
URLconf for registration and activation

"""

from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from .views import (RegistrationView,
                    UserDetailView)


urlpatterns = [
    url(r'^register/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html'
        ),
        name='registration_complete'),
    url(r'register/$',
        RegistrationView.as_view(),
        name='registration_register'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^profile/$',
        UserDetailView.as_view(), name="home"),
]
