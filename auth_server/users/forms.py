"""
Forms and valiadtion code for user registration

"""

from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

DUPLICATE_EMAIL = _("This email address is already in use. "
                    "Please provide a different email address.")

User = get_user_model()


class RegistrationForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    email = forms.EmailField(label=_("Email"), max_length=254)
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as "
                                            "before, for verification."))

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD,)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(self.cleaned_data.get('password2'))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(DUPLICATE_EMAIL)
        return self.cleaned_data['email']
