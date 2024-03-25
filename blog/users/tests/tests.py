import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User
from users.tests.fixtures import authorized_user, second_user


@pytest.mark.django_db
def test_register_user():
    user_data = {
        "email": "test@testmail.ru",
        "login": "TestUser",
        "password": "hardpassword",
        "password2": "hardpassword"
    }
    client = APIClient()
    response = client.post('/auth/signup/', user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="test@testmail.ru").exists()


@pytest.mark.django_db
def test_signin(authorized_user):
    client = authorized_user['client']
    user = authorized_user['user']

    response = client.post('/auth/signin/',
                           {'email': user.email,
                            'password': 'hardpassword'},
                           format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    assert 'refreshToken' in response.data


@pytest.mark.django_db
def test_get_registered_user(authorized_user):
    client = authorized_user['client']
    user = authorized_user['user']

    response = client.get(f'/user/{user.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == user.email
    assert response.data['login'] == user.login


@pytest.mark.django_db
def test_get_all_registered_users(authorized_user, second_user):
    client = authorized_user['client']
    user = authorized_user['user']

    response = client.get('/user/all')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    users_from_responses = [user_info['email'] for user_info in response.data]
    assert user.email in users_from_responses
    assert second_user.email in users_from_responses


@pytest.mark.django_db
def test_follower_add(authorized_user, second_user):
    client = authorized_user['client']
    response = client.post(f'/follower/add/{second_user.id}')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_follower_delete(authorized_user, second_user):
    client = authorized_user['client']
    client.post(f'/follower/add/{second_user.id}')
    response = client.delete(f'/follower/delete/{second_user.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
