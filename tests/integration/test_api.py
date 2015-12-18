# -*- coding: utf-8 -*-

# Third Party Stuff
import pytest

from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

# oAuthServer Stuff
from .. import factories

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return factories.UserFactory.create()


@pytest.fixture
def application():
    return factories.AppFactory.create()


def assert_redirect_to_login(response, next_url=None):
    login_url = reverse('auth_login')
    assert response.status_code == 302
    if next_url:
        assert "{}?next={}".format(login_url, next_url) == response['Location']
    assert login_url in response['Location']


def test_public_page_rendering(client):
    page_urls = [
        reverse('auth_login'),
        reverse('auth_logout'),
        '/',
        reverse('registration_register'),
    ]
    for path in page_urls:
        response = client.get(path)
        assert response.status_code == 200


def test_profile_page(client, user):
    url = reverse('profile')

    # Redirect to login without authrization
    response = client.get(url)
    assert_redirect_to_login(response, url)

    client.login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert user.email in response.content


def test_create_app(client, user):
    url = reverse('create_app')

    # Redirect to login in Get request if not authrized
    response = client.get(url)
    assert_redirect_to_login(response, url)

    # Redirect to login in Post request if not authrized
    response = client.post(url)
    assert_redirect_to_login(response, url)

    client.login(user)

    # App form in Get request if authorized
    response = client.get(url)
    assert response.status_code == 200
    assert "</form>" in response.content

    # Success template in Post request if authorized
    response = client.post(url, {'name': user.email, 'redirect_url': 'http://test.in'})
    assert response.status_code == 200
    assert 'Successfully' in response.content


def test_get_auth_code(client, application):
    url = reverse('get_auth_code')

    # Redirect to login in Get request if not authrized
    response = client.get(url)
    assert_redirect_to_login(response, url)

    # Redirect to login in Post request if not authrized
    response = client.post(url)
    assert_redirect_to_login(response, url)

    client.login(application.user)

    # Get Method not allowed error
    response = client.get(url)
    assert response.status_code == 405

    # auth_code in redirect_url in Post request if authorized
    response = client.post(url, {'access_key': application.access_key, 'redirect_url': application.redirect_url})
    assert response.status_code == 302
    assert 'auth_code' in response['Location']

    # error in redirect_url in Post request if authorized and wrong redirect_url given
    response = client.post(url, {'access_key': application.access_key, 'redirect_url': 'test'})
    assert response.status_code == 302
    assert 'error=invalid_request' in response['Location']

    # error in redirect_url in Post request if authorized and with missing parameters
    response = client.post(url)
    assert response.status_code == 302
    assert 'error=invalid_request' in response['Location']


def test_get_access_token(client, application):
    url = reverse('get_access_token')
    auth_code_url = reverse('get_auth_code')

    # Redirect to login in Get request if not authrized
    response = client.get(url)
    assert_redirect_to_login(response, url)

    # Redirect to login in Post request if not authrized
    response = client.post(url)
    assert_redirect_to_login(response, url)

    client.login(application.user)

    # Get Method not allowed error
    response = client.get(url)
    assert response.status_code == 405

    # auth_code in redirect_url in Post request if authorized
    response = client.post(auth_code_url, {'access_key': application.access_key,
                                           'redirect_url': application.redirect_url})
    assert response.status_code == 302
    assert 'auth_code' in response['Location']

    auth_code = response['Location'].split('auth_code=')[1].split('&')[0]

    # access_token in redirect_url in Post request if authorized and auth_code provided
    response = client.post(url, {'access_key': application.access_key, 'redirect_url': application.redirect_url,
                                 'secret_key': application.secret_key, 'auth_code': auth_code})
    assert response.status_code == 200
    assert 'access_token' in response.content

    # error in redirect_url in Post request if authorized and wrong auth_code given
    response = client.post(url, {'access_key': application.access_key, 'redirect_url': application.redirect_url,
                                 'secret_key': application.secret_key, 'auth_code': 'test'})
    assert response.status_code == 200
    assert '"error": "invalid_request"' in response.content

    # error in redirect_url in Post request if authorized and wrong secret_key given
    response = client.post(url, {'access_key': application.access_key, 'redirect_url': application.redirect_url,
                                 'secret_key': 'test', 'auth_code': auth_code})
    assert response.status_code == 200
    assert '"error": "invalid_request"' in response.content

    # error in redirect_url in Post request if authorized and with missing parameters
    response = client.post(url)
    assert response.status_code == 200
    assert '"error": "invalid_request"' in response.content


def test_resume_submission(client, application):
    url = reverse('submit_resume')
    auth_code_url = reverse('get_auth_code')
    access_token_url = reverse('get_access_token')

    # Redirect to login in Get request if not authrized
    response = client.get(url)
    assert_redirect_to_login(response, url)

    # Redirect to login in Post request if not authrized
    response = client.post(url)
    assert_redirect_to_login(response, url)

    client.login(application.user)

    # Get Method not allowed error
    response = client.get(url)
    assert response.status_code == 405

    # auth_code in redirect_url in Post request if authorized
    response = client.post(auth_code_url, {'access_key': application.access_key,
                                           'redirect_url': application.redirect_url})
    assert response.status_code == 302
    assert 'auth_code' in response['Location']

    auth_code = response['Location'].split('auth_code=')[1].split('&')[0]

    # access_token in redirect_url in Post request if authorized and auth_code provided
    response = client.post(access_token_url, {'access_key': application.access_key,
                                              'redirect_url': application.redirect_url,
                                              'secret_key': application.secret_key,
                                              'auth_code': auth_code})
    assert response.status_code == 200
    assert 'access_token' in response.content

    access_token = eval(response.content)['access_token']

    # access_token in redirect_url in Post request if authorized and access_token provided
    response = client.post(url, {'first_name': application.user.email, 'last_name': application.user.email,
                                 'project_url': application.redirect_url, 'code_url': application.redirect_url,
                                 'resume': SimpleUploadedFile('resume.txt', 'fuzzy text'),
                                 'access_token': access_token})
    assert response.status_code == 200

    # error in redirect_url in Post request if authorized and wrong access_token given
    response = client.post(url, {'first_name': application.user.email, 'last_name': application.user.email,
                                 'project_url': application.redirect_url, 'code_url': application.redirect_url,
                                 'resume': SimpleUploadedFile('resume.txt', 'fuzzy text'),
                                 'access_token': 'test'})
    assert response.status_code == 200
    assert eval(response.content)['access_token'] == ["Invalid Access Token"]

    # error in redirect_url in Post request if authorized and with missing parameters
    response = client.post(url)
    assert response.status_code == 200
    assert eval(response.content)['access_token'] == ["Missing Access Token"]
    assert eval(response.content)['resume'] == ["This field is required."]
