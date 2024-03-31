import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def authorized_user():
    user_data = {
        "email": "test@testmail.ru",
        "login": "TestUser",
        "password": "hardpassword",
        "password2": "hardpassword"
    }
    client = APIClient()
    response = client.post('/auth/signup/', user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(email='test@testmail.ru')
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return {
        'client': client,
        'user': user
    }


@pytest.fixture
def second_user():
    second_user_data = {
        'email': 'test@example.com',
        'password': 'super_hard_password',
        'login': 'second_user'
    }
    second_user = User.objects.create(
        email=second_user_data['email'],
        password=second_user_data['password'],
        login=second_user_data['login']
    )
    assert second_user.email == second_user_data['email']
    assert second_user.password == second_user_data['password']
    assert second_user.login == second_user_data['login']
    return second_user
