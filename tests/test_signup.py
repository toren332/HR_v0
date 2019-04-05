import pytest

from django.contrib.auth.models import User

from django.urls import reverse

from rest_framework.test import APIClient

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def user_of_ivan():
    return User.objects.create(username='ivan', email='ivan@test.test')


@pytest.fixture
def client():
    return APIClient()


# noinspection PyMethodMayBeStatic
class SignUpTest:
    def test_201(self, client):
        url = reverse('account-signup')

        data = {
            'username': 'username',
            'password': 'xa6eiQuoo3',
            'email': 'username@test.test',
            'kind': 'teacher',
        }
        response = client.post(url, data=data)

        assert response.status_code == 201
        assert response.data == {

        }

    def test_400(self, client, user_of_ivan):
        url = reverse('account-signup')

        data = {
            'username': 'ivan',
            'password': 'xa6eiQuoo3',
            'email': 'ivan@test.test',
            'kind': 'teacher',
        }
        response = client.post(url, data=data)

        assert response.status_code == 400
        assert response.data
