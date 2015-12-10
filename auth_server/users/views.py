"""
Views for user registration

"""

from django.contrib.auth import (authenticate,
                                 get_user_model,
                                 login)
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import DetailView

from .forms import RegistrationFormUniqueEmail
from auth_server.mixins import LoginRequiredMixin

User = get_user_model()


class RegistrationView(FormView):
    """
    Register and login a new user
    """

    form_class = RegistrationFormUniqueEmail
    success_url = None
    template_name = 'registration/registration_form.html'

    def form_valid(self, form):
        new_user = self.register(**form.cleaned_data)
        success_url = self.get_success_url(new_user)

        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def register(self, **cleaned_data):
        user_kwargs = self.get_user_kwargs(**cleaned_data)
        User.objects._create_user(**user_kwargs)

        new_user = authenticate(**{'username': user_kwargs[User.USERNAME_FIELD],
                                   'password': user_kwargs['password']})
        login(self.request, new_user)
        return new_user

    def get_success_url(self, user):
        return '/'

    def get_user_kwargs(self, **cleaned_data):
        User = get_user_model()
        return {
            User.USERNAME_FIELD: cleaned_data['email'],
            'email': cleaned_data['email'],
            'password': cleaned_data['password'],
            'is_staff': False,
            'is_superuser': False
        }


class UserDetailView(LoginRequiredMixin, DetailView):

    context_object_name = 'user_detail'
    template_name = 'profile/index.html'
    model = User

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        return context
