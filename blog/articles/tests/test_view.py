# import pytest
# from django.urls import reverse
#
# from articles.models import Article
#
#
# @pytest.mark.django_db
# def test_create_article(client):
#     url = reverse('create_article')
#     response = client.post(url)
#
#     article = Article.objects.create(
#         tags='Test', genres=['Хоррор', 'Научная фантастика']
#
#     )
