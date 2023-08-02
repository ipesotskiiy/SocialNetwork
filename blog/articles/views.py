from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response

from articles.models import Article, Genre, Comment, Rating
from articles.serializers import (
    GenreSerializer,
    ArticleSerializer,
    CommentSerializer,
    RatingSerializer
)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article = serializer.save(user_id=self.request.user)
            return Response({
                'article': ArticleSerializer(article).data
            })


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article = get_object_or_404(Article, id=self.request.data['article_id'])
            comment = serializer.save(user_id=self.request.user, article_id=article)
            return Response({
                'comment': CommentSerializer(comment).data
            })


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article = get_object_or_404(Article, id=self.request.data['article_id'])
            rating = serializer.save(user_id=self.request.user, article_id=article)
            return Response({
                'rating': RatingSerializer(rating).data
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
