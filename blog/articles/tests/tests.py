import pytest
from rest_framework import status

from articles.models import Article
from users.tests.fixtures import authorized_user
from articles.tests.fixtures import created_article, created_comment


@pytest.mark.django_db
def test_create_article(authorized_user):
    client = authorized_user['client']
    article_info = {"title": "Test title",
                    "text": "Test text",
                    "genres": [{"name": "Хоррор"}],
                    "tags": [{"name": "Test tag"}]}

    response = client.post('/article/add', article_info, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Article.objects.filter(title='Test title').exists()


@pytest.mark.django_db
def test_get_article(authorized_user, created_article):
    client = authorized_user['client']
    response = client.get(f'/article/{created_article.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == created_article.title
    assert response.data['text'] == created_article.text


@pytest.mark.django_db
def test_get_all_articles(authorized_user, created_article):
    client = authorized_user['client']

    second_article_info = {"title": "Test title2",
                           "text": "Test text",
                           "genres": [{"name": "Научная фантастика"}],
                           "tags": [{"name": "Test tag"}]}

    response = client.post('/article/add', second_article_info, format='json')

    assert response.status_code == status.HTTP_201_CREATED

    second_response = client.get('/article/all')
    assert second_response.status_code == status.HTTP_200_OK
    assert len(second_response.data) == 2


@pytest.mark.django_db
def test_update_article(authorized_user, created_article):
    client = authorized_user['client']
    response = client.patch(f'/article/update/{created_article.id}', {"title": "New test title"}, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == "New test title"


@pytest.mark.django_db
def test_delete_article(authorized_user, created_article):
    client = authorized_user['client']
    response = client.delete(f'/article/delete/{created_article.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None


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
