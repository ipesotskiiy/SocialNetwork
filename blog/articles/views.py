from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from articles.models import Article, Genre
from articles.serializers import ReadArticleSerializer, GenreSerializer, WriteArticleSerializer


class OneArticleView(generics.RetrieveAPIView):
    def get(self, request, id):
        article = Article.objects.get(pk=self.kwargs['id'])
        article_serializer = ReadArticleSerializer(article)
        return Response({
            'article': article_serializer.data
        })


class AllArticlesView(generics.ListAPIView):

    def get(self, request):
        articles = self.filter_queryset(Article.objects.all())
        articles_serializer = ReadArticleSerializer(articles, many=True)
        return Response({
            'articles': articles_serializer.data
        })


class CreateArticleView(generics.CreateAPIView):
    serializer_class = WriteArticleSerializer

    def post(self, request, *args, **kwargs):
        login = request.user.login
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article = serializer.save(user_id=self.request.user)
            return Response({
                'article': WriteArticleSerializer(article).data
            })


class OneGenreView(generics.RetrieveAPIView):
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
