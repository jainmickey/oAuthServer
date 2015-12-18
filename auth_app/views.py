from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import (App,
                     AccessToken,
                     Grant,
                     Submission)
from .utils import (generate_token,
                    redirect_util)
from . import forms


@login_required
def createApplication(request, form_class=forms.CreateAppForm):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data.get("name")
            redirect_url = form.cleaned_data.get("redirect_url")
            App.objects.create(user=user, name=name,
                               redirect_url=redirect_url,
                               access_key=generate_token(),
                               secret_key=generate_token())
            return render(request, "auth_app/create_app_success.html")
    else:
        form = form_class()

    return render(request, "auth_app/create_app.html",
                  {"form": form})


@csrf_exempt
@login_required
@require_POST
def getAuthorizationCode(request, form_class=forms.ClientAuthForm):
    form = form_class(request.POST)
    if form.is_valid():
        application = form.cleaned_data.get("application")
        Grant.objects.filter(app=application,
                             user=request.user).delete()
        auth_code = Grant.objects.create(app=application,
                                         user=request.user,
                                         token=generate_token())
        params = {"auth_code": auth_code.token}
        if form.cleaned_data["state"]:
            params.update({"state": form.cleaned_data["state"]})
        return redirect_util(application.redirect_url, params)
    else:
        if form.errors.get("access_key"):
            error_desc = form.errors.get("access_key")[0]
        elif form.errors.get("redirect_url"):
            error_desc = form.errors.get("redirect_url")[0]
        else:
            error_desc = form.errors.get("__all__")[0]

        application = form.cleaned_data.get("application")
        if application:
            return redirect_util(application.redirect_url,
                                 {"error": "invalid_request",
                                  "error_description": error_desc})
        else:
            return redirect_util(request.META.get("REFERER", "/"),
                                 {"error": "invalid_request",
                                  "error_description": error_desc})


@csrf_exempt
@login_required
@require_POST
def getAccessToken(request, form_class=forms.AccessTokenForm):
    form = form_class(request.POST)
    if form.is_valid():
        grant = form.cleaned_data.get("grant")
        AccessToken.objects.filter(user=grant.user,
                                   app=grant.app).delete()
        access_token = AccessToken.objects.create(user=grant.user,
                                                  app=grant.app,
                                                  token=generate_token())
        params = {
            "access_token": access_token.token
        }
        return JsonResponse(params)
    else:
        if form.errors.get("access_key"):
            error_desc = form.errors.get("access_key")[0]
        elif form.errors.get("redirect_url"):
            error_desc = form.errors.get("redirect_url")[0]
        elif form.errors.get("auth_code"):
            error_desc = form.errors.get("auth_code")[0]
        elif form.errors.get("secret_key"):
            error_desc = form.errors.get("secret_key")[0]
        else:
            error_desc = form.errors.get("__all__")[0]

        return JsonResponse({"error": "invalid_request",
                             "error_description": error_desc})


@csrf_exempt
@login_required
@require_POST
def submitResume(request, form_class=forms.ResumeSubmissionForm):
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        user = form.cleaned_data.get("access_token").user
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")
        user.save()
        user.project_url = form.cleaned_data["project_url"]
        user.code_url = form.cleaned_data["code_url"]
        user.save()
        Submission.objects.filter(user=user).delete()
        Submission.objects.create(user=user,
                                  resume=form.cleaned_data["resume"])
        return JsonResponse({"success": True})
    return JsonResponse(form.errors)
