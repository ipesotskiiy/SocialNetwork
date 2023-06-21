from django.urls import path

from articles.views import (
    AllArticlesView,
    OneArticleView,
    OneGenreView,
    AllGenresView,
    CreateArticleView,
    UpdateArticleView,
    DeleteArticleView
)

app_name = 'articles'

urlpatterns = [
    path('genre/all', AllGenresView.as_view(), name='genres'),
    path('article/all', AllArticlesView.as_view(), name='articles'),
    path('article/add', CreateArticleView.as_view(), name='create_article'),
    path('article/<id>', OneArticleView.as_view(), name='article'),
    path('article/update/<id>', UpdateArticleView.as_view(), name='update_article'),
    path('article/delete/<id>', DeleteArticleView.as_view(), name='delete_article'),
    path('genre/<id>', OneGenreView.as_view(), name='genre')
]