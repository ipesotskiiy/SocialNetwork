from django.urls import path

from articles.views import AllArticlesView, OneArticleView, OneGenreView, AllGenresView

app_name = 'articles'

urlpatterns = [
    path('genre/all', AllGenresView.as_view(), name='genres'),
    path('article/all', AllArticlesView.as_view(), name='articles'),
    path('article/<id>', OneArticleView.as_view(), name='article'),
    path('genre/<id>', OneGenreView.as_view(), name='genre')
]