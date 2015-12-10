from django import forms

from .models import (App, Grant, AccessToken)
from .utils import Errors


class ClientAuthForm(forms.Form):
    """
    Client authentication form. Required to make sure that we're dealing with a
    real client.
    """
    access_key = forms.CharField(error_messages={"required": Errors["invalid_client"][0]})
    redirect_url = forms.URLField(error_messages={"required": Errors["invalid_request"][0]})
    state = forms.CharField(required=False)

    def clean(self):
        data = self.cleaned_data
        if data.get("access_key"):
            application = App.objects.filter(access_key__iexact=data.get("access_key"))
            if application:
                data["application"] = application[0]
                if data.get("redirect_url"):
                    if (data["application"].redirect_url != data.get("redirect_url")):
                        raise forms.ValidationError(Errors["invalid_request"][1])
            else:
                raise forms.ValidationError(Errors["invalid_client"][1])
        return data


class AccessTokenForm(forms.Form):
    """
    Access token form. Required to authenticate client.
    """
    access_key = forms.CharField(error_messages={"required": Errors["invalid_client"][0]})
    redirect_url = forms.URLField(error_messages={"required": Errors["invalid_request"][0]})
    auth_code = forms.CharField(error_messages={"required": Errors["invalid_request"][2]})
    secret_key = forms.CharField(error_messages={"required": Errors["invalid_request"][4]})

    def clean(self):
        data = self.cleaned_data
        if data.get("access_key"):
            application = App.objects.filter(access_key__iexact=data.get("access_key"))
            if application:
                data["application"] = application[0]
                if data.get("redirect_url"):
                    if (data["application"].redirect_url != data.get("redirect_url")):
                        raise forms.ValidationError(Errors["invalid_request"][1])
            else:
                raise forms.ValidationError(Errors["invalid_client"][1])

            if data.get("auth_code"):
                grant = Grant.objects.filter(token__iexact=data.get("auth_code"))
                if ((not grant) or (grant[0].app.access_key != data.get("access_key")) or
                   (grant[0].app.redirect_url != data.get("redirect_url"))):
                    raise forms.ValidationError(Errors["invalid_request"][3])
                if data.get("secret_key"):
                    if (grant[0].app.secret_key != data.get("secret_key")):
                        raise forms.ValidationError(Errors["invalid_request"][5])

                data["grant"] = grant[0]
        return data


class ClientAppForm(forms.Form):
    """
    """
    name = forms.CharField(max_length=50)
    redirect_url = forms.URLField()


class ResumeSubmissionForm(forms.Form):
    """
    """
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    projects_url = forms.URLField()
    code_url = forms.URLField()
    resume = forms.FileField()
    access_token = forms.CharField(error_messages={"required": Errors["invalid_request"][6]})

    def clean_access_token(self):
        data = self.cleaned_data
        access_token = None
        if data.get("access_token"):
            access_token = AccessToken.objects.filter(token__iexact=access_token)
        if not access_token:
            raise forms.ValidationError(Errors["invalid_request"][7])
        return access_token[0]
