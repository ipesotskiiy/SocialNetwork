from django.urls import path

from articles.views import (
    AllArticlesView,
    OneArticleView,
    OneGenreView,
    AllGenresView,
    CreateArticleView,
    UpdateArticleView,
    DeleteArticleView,
    CreateCommentView,
    ReadCommentView,
    ReadAllCommentsView,
    UpdateCommentView, DeleteCommentView
)

app_name = 'articles'

urlpatterns = [
    path('genre/all', AllGenresView.as_view(), name='genres'),
    path('article/all', AllArticlesView.as_view(), name='articles'),
    path('comments/all', ReadAllCommentsView.as_view(), name='comments'),
    path('article/add', CreateArticleView.as_view(), name='create_article'),
    path('comment/add', CreateCommentView.as_view(), name='create_comment'),
    path('comment/<id>', ReadCommentView.as_view(), name='comment'),
    path('article/<id>', OneArticleView.as_view(), name='article'),
    path('article/update/<id>', UpdateArticleView.as_view(), name='update_article'),
    path('comment/update/<id>', UpdateCommentView.as_view(), name='update_comment'),
    path('article/delete/<id>', DeleteArticleView.as_view(), name='delete_article'),
    path('comment/delete/<id>', DeleteCommentView.as_view(), name='delete_comment'),
    path('genre/<id>', OneGenreView.as_view(), name='genre')
]
