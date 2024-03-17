from django.urls import path

from articles.views import (
    ArticleViewSet,
    CommentViewSet,
    RatingViewSet,
    LikeListCreate,
    DislikeListCreate,
    GenreViewSet,
    TagViewSet
)

app_name = 'articles'

urlpatterns = [
    path('article/all', ArticleViewSet.as_view({'get': 'list'}), name='articles'),
    path('comment/all', CommentViewSet.as_view({'get': 'list'})),
    path('rating/all', RatingViewSet.as_view({'get': 'list'})),
    path('genre/all', GenreViewSet.as_view({'get': 'list'})),
    path('tag/all', TagViewSet.as_view({'get': 'list'})),
    path('article/add', ArticleViewSet.as_view({'post': 'create'}), name='create_article'),
    path('comment/add', CommentViewSet.as_view({'post': 'create'})),
    path('rating/add', RatingViewSet.as_view({'post': 'create'})),
    path('genre/add', GenreViewSet.as_view({'post': 'create'})),
    path('tag/add', TagViewSet.as_view({'post': 'create'})),
    path('comment/<pk>', CommentViewSet.as_view({'get': 'retrieve'})),
    path('article/<pk>', ArticleViewSet.as_view({'get': 'retrieve'}), name='article'),
    path('rating/<pk>', RatingViewSet.as_view({'get': 'retrieve'})),
    path('genre/<pk>', GenreViewSet.as_view({'get': 'retrieve'})),
    path('tag/<pk>', TagViewSet.as_view({'get': 'retrieve'})),
    path('article/update/<pk>', ArticleViewSet.as_view({'patch': 'partial_update'})),
    path('comment/update/<pk>', CommentViewSet.as_view({'patch': 'partial_update'})),
    path('rating/update/<pk>', RatingViewSet.as_view({'patch': 'partial_update'})),
    path('genre/update/pk', GenreViewSet.as_view({'patch': 'partial_update'})),
    path('tag/update/<pk>', TagViewSet.as_view({'patch': 'partial_update'})),
    path('article/delete/<pk>', ArticleViewSet.as_view({'delete': 'destroy'})),
    path('comment/delete/<pk>', CommentViewSet.as_view({'delete': 'destroy'})),
    path('rating/delete/<pk>', RatingViewSet.as_view({'delete': 'destroy'})),
    path('genre/delete/<pk>', GenreViewSet.as_view({'delete': 'destroy'})),
    path('tag/delete/<pk>', TagViewSet.as_view({'delete': 'destroy'})),
    path('comment/like/<int:pk>', LikeListCreate.as_view(), name='comment_likes'),
    path('comment/dislike/<int:pk>', DislikeListCreate.as_view(), name='comment_dislikes'),
]
