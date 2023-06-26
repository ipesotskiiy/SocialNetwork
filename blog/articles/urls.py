from django.urls import path

from articles.views import (
    OneGenreView,
    AllGenresView,
    ArticleViewSet,
    CommentViewSet
)

app_name = 'articles'

urlpatterns = [
    path('genre/all', AllGenresView.as_view(), name='genres'),
    path('article/all', ArticleViewSet.as_view({'get': 'list'}), name='articles2'),
    path('comment/all2', CommentViewSet.as_view({'get': 'list'})),
    path('article/add', ArticleViewSet.as_view({'post': 'create'})),
    path('comment/add2', CommentViewSet.as_view({'post': 'create'})),
    path('comment2/<pk>', CommentViewSet.as_view({'get': 'retrieve'})),
    path('article/<id>', ArticleViewSet.as_view({'get': 'retrieve'}), name='article2'),
    path('article/update/<pk>', ArticleViewSet.as_view({'patch': 'partial_update'})),
    path('comment/update2/<pk>', CommentViewSet.as_view({'patch': 'partial_update'})),
    path('article/delete/<pk>', ArticleViewSet.as_view({'delete': 'destroy'})),
    path('comment/delete/<pk>', CommentViewSet.as_view({'delete': 'destroy'})),
    path('genre/<id>', OneGenreView.as_view(), name='genre')
]
