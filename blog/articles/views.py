from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
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

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]

        return super(ArticleViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article = serializer.save(user_id=self.request.user)

            return Response({
                'article': ArticleSerializer(article).data
            }, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user_id
        user.count_article -= 1
        user.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            }, status=status.HTTP_201_CREATED)


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
            }, status=status.HTTP_201_CREATED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class LikeListCreate(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        like_count = Like.objects.filter(comment_id=comment).count()
        return Response({"like count": like_count})

    def post(self, request, pk):
        user_id = request.user
        comment = get_object_or_404(Comment, pk=pk)

        existing_dislike = Dislike.objects.filter(user_id=user_id, comment_id=comment)
        if existing_dislike.exists():
            existing_dislike.delete()

        existing_like = Like.objects.filter(user_id=user_id, comment_id=comment)
        if existing_like.exists():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Already Liked"
            })

        like = Like.objects.create(comment_id=comment)
        like.user_id.add(user_id)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DislikeListCreate(APIView):

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        dislike_count = Dislike.objects.filter(comment_id=comment).count()
        return Response({"dislike count": dislike_count})

    def post(self, request, pk):
        user_id = request.user
        comment = get_object_or_404(Comment, pk=pk)

        existing_like = Like.objects.filter(user_id=user_id, comment_id=comment)
        if existing_like.exists():
            existing_like.delete()

        existing_dislike = Dislike.objects.filter(user_id=user_id, comment_id=comment)
        if existing_dislike.exists():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Already Disliked"
            })

        dislike = Dislike.objects.create(comment_id=comment)
        dislike.user_id.add(user_id)
        serializer = DislikeSerializer(dislike)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
