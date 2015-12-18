# -*- coding: utf-8 -*-

# Third Party Stuff
import factory
from django.conf import settings

from auth_app import models as app_models


class Factory(factory.DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True


class UserFactory(Factory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    email = factory.Sequence(lambda n: 'user%04d@email.com' % n)
    password = factory.PostGeneration(lambda obj, *args, **kwargs: obj.set_password('123123'))


def create_user(**kwargs):
    "Create an user along with their dependencies"
    return UserFactory.create(**kwargs)


class AppFactory(Factory):
    class Meta:
        model = app_models.App

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: "App%s" % n)
    access_key = factory.Sequence(lambda n: "AccessKey_%s" % n)
    secret_key = factory.Sequence(lambda n: "SecretKey_%s" % n)
    redirect_url = factory.LazyAttribute(lambda obj: 'http://%s.in' % obj.name)


class GrantFactory(Factory):
    class Meta:
        model = app_models.Grant

    user = factory.SubFactory(UserFactory)
    app = factory.SubFactory(AppFactory)


class AccessTokenFactory(Factory):
    class Meta:
        model = app_models.AccessToken

    user = factory.SubFactory(UserFactory)
    app = factory.SubFactory(AppFactory)


class SubmissionFactory(Factory):
    class Meta:
        model = app_models.Submission

    user = factory.SubFactory(UserFactory)
    resume = factory.django.FileField(text=factory.Sequence(lambda n: "Resume_#%s" % n))
