from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from articles.filters import ArticleFilter
from articles.models import Article, Genre, Comment, Rating, Like, Dislike, Tag
from articles.serializers import (
    GenreSerializer,
    ArticleSerializer,
    CommentSerializer,
    RatingSerializer,
    LikeSerializer,
    DislikeSerializer,
    TagSerializer
)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

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


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class LikeListCreate(APIView):

    def get(self, request, pk):
        comment = Comment.objects.filter(pk=pk)
        like_count = comment.comment_id.count()
        serializer = LikeSerializer(like_count, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        user_id = self.request.user
        comment_id = Comment.objects.filter(pk=pk)
        check = Like.objects.filter(Q(user_id=user_id) & Q(comment_id=comment_id.last()))
        if (check.exists()):
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Already Liked"
            })
        new_like = Like.objects.create(comment_id=comment_id.last())
        new_like.save()
        new_like.user_id.set([request.user])
        serializer = LikeSerializer(new_like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DislikeListCreate(APIView):

    def get(self, request, pk):
        comment = Comment.objects.filter(pk=pk)
        dislike_count = comment.comment_id.count()
        serializer = DislikeSerializer(dislike_count, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        user_id = self.request.user
        comment_id = Comment.objects.filter(pk=pk)
        check = Dislike.objects.filter(Q(user_id=user_id) & Q(comment_id=comment_id.last()))
        if (check.exists()):
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Already Disliked"
            })
        new_like = Dislike.objects.create(comment_id=comment_id.last())
        new_like.save()
        new_like.user_id.set([request.user])
        serializer = DislikeSerializer(new_like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# class OneGenreView(generics.RetrieveAPIView):
#     serializer_class = GenreSerializer
#
#     def get(self, request, id):
#         genre = Genre.objects.get(pk=self.kwargs['id'])
#         genre_serializer = GenreSerializer(genre)
#         return Response({
#             'genre': genre_serializer.data
#         })
#
#
# class AllGenresView(generics.ListAPIView):
#     serializer_class = GenreSerializer
#
#     def get(self, request):
#         genres = Genre.objects.all()
#         genres_serializer = GenreSerializer(genres, many=True)
#         return Response({
#             'genres': genres_serializer.data
#         })
