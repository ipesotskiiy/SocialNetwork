import pytest
from rest_framework import status

from users.tests.fixtures import authorized_user
from articles.tests.fixtures import created_genre


@pytest.mark.django_db
def test_create_genre(authorized_user):
    client = authorized_user['client']
    genre_name = {"name": "Хоррор"}
    response = client.post('/genre/add', genre_name, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == genre_name['name']


@pytest.mark.django_db
def test_not_create_genre(authorized_user):
    client = authorized_user['client']
    genre_name = {"name": "Not valid name for genre"}
    response = client.post('/genre/add', genre_name, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_genre(authorized_user, created_genre):
    client = authorized_user['client']
    response = client.get(f'/genre/{created_genre.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == created_genre.id


@pytest.mark.django_db
def test_get_all_genres(authorized_user, created_genre):
    client = authorized_user['client']
    genre_name = {"name": "Научная фантастика"}
    response = client.post('/genre/add', genre_name, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    second_response = client.get('/genre/all')
    assert second_response.status_code == status.HTTP_200_OK
    assert len(second_response.data) == 2


@pytest.mark.django_db
def test_update_genre(authorized_user, created_genre):
    client = authorized_user['client']
    new_genre_name = {"name": "Фентези"}
    response = client.patch(f'/genre/update/{created_genre.id}', new_genre_name, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == new_genre_name['name']


@pytest.mark.django_db
def test_not_update_genre(authorized_user, created_genre):
    client = authorized_user['client']
    new_genre_name = {"name": "Not valid name"}
    response = client.patch(f'/genre/update/{created_genre.id}', new_genre_name, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_genre(authorized_user, created_genre):
    client = authorized_user['client']
    response = client.delete(f'/genre/delete/{created_genre.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
