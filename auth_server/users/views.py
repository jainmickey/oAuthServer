"""
Views for user registration

"""

from django.contrib.auth import (authenticate,
                                 get_user_model,
                                 login)
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from .forms import RegistrationFormUniqueEmail

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
