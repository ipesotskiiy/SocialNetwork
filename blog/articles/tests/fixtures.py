import pytest
from rest_framework import status

from articles.models import Article, Comment
from users.tests.fixtures import authorized_user


@pytest.fixture
def created_article(authorized_user):
    client = authorized_user['client']
    article_info = {"title": "Test title",
                    "text": "Test text",
                    "genres": [{"name": "Хоррор"}],
                    "tags": [{"name": "Test tag"}]}

    response = client.post('/article/add', article_info, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Article.objects.filter(title='Test title').exists()
    article = Article.objects.get(title='Test title')
    return article


@pytest.fixture
def created_comment(authorized_user, created_article):
    client = authorized_user['client']
    for_comment = {"article_id": created_article.id, "text": "New comment"}
    response = client.post('/comment/add', for_comment, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    comment = Comment.objects.get(pk=response.data['comment']['id'])
    return comment
