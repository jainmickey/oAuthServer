# -*- coding: utf-8 -*-
# Third Party Stuff
from django.test import TestCase

from .models import User


class UserModelTestCase(TestCase):

    def test_create_user(self):
        u = User.objects.create_user(email='f@F.com', password='abc', first_name="F", last_name='B',
                                     project_url='http://test.in', code_url='http://test.in')
        assert u.is_active is True
        assert u.is_staff is False
        assert u.is_superuser is False
        assert u.email == 'f@f.com'
        assert u.project_url == u.code_url == 'http://test.in'
        assert u.get_full_name() == 'F B'
        assert u.get_short_name() == 'F'
        assert str(u) == str(u.id)

    def test_create_super_user(self):
        u = User.objects.create_superuser(email='f@f.com', password='abc')
        assert u.is_active is True
        assert u.is_staff is True
        assert u.is_superuser is True
        assert str(u) == str(u.id)
