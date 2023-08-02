from django.urls import path

from articles.views import (
    OneGenreView,
    AllGenresView,
    ArticleViewSet,
    CommentViewSet, RatingViewSet
)

app_name = 'articles'

urlpatterns = [
    path('genre/all', AllGenresView.as_view(), name='genres'),
    path('article/all', ArticleViewSet.as_view({'get': 'list'}), name='articles'),
    path('comment/all', CommentViewSet.as_view({'get': 'list'})),
    path('rating/all', RatingViewSet.as_view({'get': 'list'})),
    path('article/add', ArticleViewSet.as_view({'post': 'create'})),
    path('comment/add', CommentViewSet.as_view({'post': 'create'})),
    path('rating/add', RatingViewSet.as_view({'post': 'create'})),
    path('comment/<pk>', CommentViewSet.as_view({'get': 'retrieve'})),
    path('article/<pk>', ArticleViewSet.as_view({'get': 'retrieve'}), name='article'),
    path('rating/<pk>', RatingViewSet.as_view({'get': 'retrieve'})),
    path('article/update/<pk>', ArticleViewSet.as_view({'patch': 'partial_update'})),
    path('comment/update/<pk>', CommentViewSet.as_view({'patch': 'partial_update'})),
    path('rating/update/<pk>', RatingViewSet.as_view({'patch': 'partial_update'})),
    path('article/delete/<pk>', ArticleViewSet.as_view({'delete': 'destroy'})),
    path('comment/delete/<pk>', CommentViewSet.as_view({'delete': 'destroy'})),
    path('rating/delete/<pk>', RatingViewSet.as_view({'delete': 'destroy'})),
    path('genre/<id>', OneGenreView.as_view(), name='genre')
]
