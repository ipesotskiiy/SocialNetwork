from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import Article, Genre
from articles.serializers import (
    ReadArticleSerializer,
    GenreSerializer,
    WriteAndUpdateArticleSerializer)


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
    serializer_class = WriteAndUpdateArticleSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article = serializer.save(user_id=self.request.user)
            return Response({
                'article': WriteAndUpdateArticleSerializer(article).data
            })


class UpdateArticleView(APIView):
    def patch(self, request, id, *args, **kwargs):
        article = Article.objects.get(pk=id)
        serializer = WriteAndUpdateArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'article': WriteAndUpdateArticleSerializer(article).data
            })


class DeleteArticleView(APIView):
    def delete(self, request, id, *args, **kwargs):
        article = Article.objects.get(pk=id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
