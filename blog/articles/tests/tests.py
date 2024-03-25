import pytest
from rest_framework import status

from articles.models import Article
from users.tests.fixtures import authorized_user


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
