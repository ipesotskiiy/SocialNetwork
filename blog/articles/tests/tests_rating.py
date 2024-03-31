import pytest
from rest_framework import status
from users.tests.fixtures import authorized_user
from articles.tests.fixtures import created_article, created_rating


@pytest.mark.django_db
def test_get_rating(authorized_user, created_rating):
    client = authorized_user['client']
    response = client.get(f'/rating/{created_rating.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == created_rating.id


@pytest.mark.django_db
def test_get_sll_ratings(authorized_user, created_article, created_rating):
    client = authorized_user['client']
    for_rating = {"article_id": created_article.id, "rating": 5}
    response = client.post('/rating/add', for_rating, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['rating']['rating'] == for_rating['rating']

    second_response = client.get('/rating/all')
    assert second_response.status_code == status.HTTP_200_OK
    assert len(second_response.data) == 2


@pytest.mark.django_db
def test_update_rating(authorized_user, created_rating):
    client = authorized_user['client']
    response = client.patch(f'/rating/update/{created_rating.id}', {"rating": 4}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['rating'] == 4


@pytest.mark.django_db
def test_delete_rating(authorized_user, created_rating):
    client = authorized_user['client']
    response = client.delete(f'/rating/delete/{created_rating.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
