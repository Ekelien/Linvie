import pytest

from linvie import create_app


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.          # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False  # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='super', password='super0000'):
        return self._client.post(
            'user/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/user/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
