# -*- coding: utf-8 -*-

# Third Party Stuff
from django.test import TestCase

# oAuthServer Stuff
from .. import factories


class TestApp(TestCase):
    def test_app_returns_str(self):
        app = factories.AppFactory.build()
        self.assertEqual(str(app), '{}'.format(app.name))


class TestGrant(TestCase):
    def test_grant_returns_str(self):
        grant = factories.GrantFactory.build()
        self.assertEqual(str(grant), '{}'.format(grant.token))


class TestAccessToken(TestCase):
    def test_access_token_returns_str(self):
        access_token = factories.AccessTokenFactory.build()
        self.assertEqual(str(access_token), '{}'.format(access_token.token))


class TestSubmission(TestCase):
    def test_submission_returns_str(self):
        submission = factories.SubmissionFactory.build()
        self.assertEqual(str(submission), '{}'.format(submission.user.email))
