from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from rest_framework.views import APIView

from articles.models import Article, Genre
from articles.serializers import ArticleSerializer, GenreSerializer


class OneArticleView(generics.ListAPIView):
    def get(self, request, id):
        article = Article.objects.get(pk=self.kwargs['id'])
        article_serializer = ArticleSerializer(article)
        return Response({
            'article': article_serializer.data
        })


class AllArticlesView(generics.ListAPIView):

    def get(self, request):
        articles = self.filter_queryset(Article.objects.all())
        articles_serializer = ArticleSerializer(articles, many=True)
        return Response({
            'articles': articles_serializer.data
        })


class OneGenreView(generics.ListAPIView):
    def get(self, request, id):
        genre = Genre.objects.get(pk=self.kwargs['id'])
        genre_serializer = GenreSerializer(genre)
        return Response({
            'genre': genre_serializer.data
        })


class AllGenresView(generics.ListAPIView):
    def get(self, request):
        genres = Genre.objects.all()
        genres_serializer = GenreSerializer(genres, many=True)
        return Response({
            'genres': genres_serializer.data
        })
