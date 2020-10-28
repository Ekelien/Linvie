from os import environ

import pytest
from dotenv import load_dotenv
from flask import session

load_dotenv()


def test_dotenv_config():
    assert environ.get('FLASK_APP') == 'wsgi.py'


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"ENTER" in response.data


def test_first_click_user(client):
    response = client.get('/user/check')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/user/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b"Your password must contain at least 8 characters, with at least one letter and one digit."),
        ('super', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/user/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/user/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/home'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'super'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_login_required_to_comment(client):
    response = client.post('/comment?id=0')
    assert response.headers['Location'] == 'http://localhost/user/login'
