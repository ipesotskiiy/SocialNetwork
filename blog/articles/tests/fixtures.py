import pytest
from rest_framework import status

from articles.models import Article, Comment, Rating, Genre
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


@pytest.fixture
def created_rating(authorized_user, created_article):
    client = authorized_user['client']
    for_rating = {"article_id": created_article.id, "rating": 5}
    response = client.post('/rating/add', for_rating, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    rating = Rating.objects.get(pk=response.data['rating']['id'])
    return rating


@pytest.fixture
def created_genre(authorized_user):
    client = authorized_user['client']
    genre_name = {"name": "Хоррор"}
    response = client.post('/genre/add', genre_name, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    genre = Genre.objects.get(pk=response.data['id'])
    return genre

