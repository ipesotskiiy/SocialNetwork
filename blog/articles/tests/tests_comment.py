import pytest
from rest_framework import status
from users.tests.fixtures import authorized_user
from articles.tests.fixtures import created_article, created_comment


@pytest.mark.django_db
def test_comment_add(authorized_user, created_article):
    client = authorized_user['client']
    for_comment = {"article_id": created_article.id, "text": "New comment"}
    response = client.post('/comment/add', for_comment, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['comment']['text'] == for_comment['text']


@pytest.mark.django_db
def test_get_comment(authorized_user, created_comment):
    client = authorized_user['client']
    response = client.get(f'/comment/{created_comment.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == created_comment.id


@pytest.mark.django_db
def test_get_all_comments(authorized_user, created_article, created_comment):
    client = authorized_user['client']
    for_second_comment = {"article_id": created_article.id, "text": "New second comment"}
    response = client.post('/comment/add', for_second_comment, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['comment']['text'] == for_second_comment['text']

    second_response = client.get('/comment/all')

    assert second_response.status_code == status.HTTP_200_OK
    assert len(second_response.data) == 2


@pytest.mark.django_db
def test_update_comment(authorized_user, created_comment):
    client = authorized_user['client']
    response = client.patch(f'/comment/update/{created_comment.id}', {"text": 'Update comment'}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['text'] == 'Update comment'


@pytest.mark.django_db
def test_delete_comment(authorized_user, created_comment):
    client = authorized_user['client']
    response = client.delete(f'/comment/delete/{created_comment.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
