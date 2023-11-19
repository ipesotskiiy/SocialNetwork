from django_filters import (
    BaseInFilter,
    CharFilter,
    FilterSet,
)

from articles.models import Article


class CharFilterInFilter(BaseInFilter, CharFilter):
    pass


class ArticleFilter(FilterSet):
    genres = CharFilterInFilter(field_name='genres__id', lookup_expr='in')
    tags = CharFilterInFilter(field_name='tags__name', lookup_expr='in')

    class Meta:
        model = Article
        fields = ['genres', 'tags']
