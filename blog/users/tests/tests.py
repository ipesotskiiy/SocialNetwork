import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from rest_framework.test import APIClient


@pytest.fixture
def for_register_user():
    return {
        "email": "test@testmail.ru",
        "login": "TestUser",
        "password": "hardpassword",
        "password2": "hardpassword"
    }


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



@pytest.mark.django_db
def test_register_user(for_register_user):
    client = APIClient()
    response = client.post('/auth/signup/', for_register_user, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="test@testmail.ru").exists()


@pytest.mark.django_db
def test_get_registered_user(authorized_user):
    client = authorized_user['client']
    user = authorized_user['user']

    # Отправка запроса на получение данных пользователя
    response = client.get(f'/user/{user.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == user.email
    assert response.data['login'] == user.login
