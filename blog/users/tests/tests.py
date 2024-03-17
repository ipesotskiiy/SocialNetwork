import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from rest_framework.test import APIClient
@pytest.fixture
def user_registration_data():
    return {
        "email": "test@testmail.ru",
        "login": "TestUser",
        "password": "hardpassword",
        "password2": "hardpassword"
    }

@pytest.mark.django_db
def test_register_user(user_registration_data):
    client = APIClient()
    response = client.post('/auth/signup/', user_registration_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="test@testmail.ru").exists()


@pytest.mark.django_db
def test_get_user(user_registration_data):
    client = APIClient()
    response = client.post('/auth/signup', user_registration_data)

    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(email=user_registration_data['email'])
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    retrieve_response = client.get(f'/user/{user.id}')

    assert retrieve_response.status_code == status.HTTP_200_OK
    assert retrieve_response.data['email'] == user_registration_data['email']
    assert retrieve_response.data['login'] == user_registration_data['login']