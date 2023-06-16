from rest_framework import serializers

from articles.models import Article, Genre


class ArticleSerializer(serializers.ModelSerializer):
    article_id = serializers.SerializerMethodField('get_id')

    class Meta:
        depth = 1
        model = Article
        fields = (
            '__all__'
        )

    def get_id(self, obj):
        return obj.id


class GenreSerializer(serializers.ModelSerializer):
    genre_id = serializers.SerializerMethodField('get_id')

    class Meta:
        model = Genre
        fields = ('name',
                  'genre_id')

    def get_id(self, obj):
        return obj.id
