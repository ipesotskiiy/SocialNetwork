import pytest
from rest_framework import status

from users.tests.fixtures import authorized_user
from articles.tests.fixtures import created_tag


@pytest.mark.django_db
def test_get_genre(authorized_user, created_tag):
    client = authorized_user['client']
    response = client.get(f'/tag/{created_tag.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == created_tag.id


@pytest.mark.django_db
def test_get_all_genres(authorized_user, created_tag):
    client = authorized_user['client']
    for_new_tag = {"name": "New test tag name"}
    response = client.post('/tag/add', for_new_tag, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == for_new_tag['name']

    second_response = client.get('/tag/all', for_new_tag, format='json')
    assert second_response.status_code == status.HTTP_200_OK
    assert len(second_response.data) == 2


@pytest.mark.django_db
def test_update_genre(authorized_user, created_tag):
    client = authorized_user['client']
    for_update_tag = {"name": "New tag name"}
    response = client.patch(f'/tag/update/{created_tag.id}', for_update_tag, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == for_update_tag['name']


@pytest.mark.django_db
def test_delete_genre(authorized_user, created_tag):
    client = authorized_user['client']
    response = client.delete(f'/tag/delete/{created_tag.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
