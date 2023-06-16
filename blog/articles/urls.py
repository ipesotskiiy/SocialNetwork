from django.urls import path

from articles.views import AllArticlesView, OneArticleView

app_name = 'articles'

urlpatterns = [
    path('articles/all', AllArticlesView.as_view(), name='all'),
    path('articles/<id>', OneArticleView.as_view(), name='article')
]