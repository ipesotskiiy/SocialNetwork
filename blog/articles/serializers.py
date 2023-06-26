from datetime import datetime

from rest_framework import serializers

from articles.models import Article, Genre, Comment


class ArticleSerializer(serializers.ModelSerializer):
    article_id = serializers.SerializerMethodField('get_id')
    login = serializers.ReadOnlyField(source='user.login')
    publication_date = serializers.DateTimeField(default=datetime.now(), read_only=True)
    average_rate = serializers.SerializerMethodField('calculate_average_rate', default=0.0, read_only=True)
    count_like = serializers.IntegerField(default=0, read_only=True)
    count_dislike = serializers.IntegerField(default=0, read_only=True)

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


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.SerializerMethodField('get_id')
    date = serializers.DateTimeField(required=False, default=datetime.now(), format="%Y-%m-%d %H:%M:%S", read_only=True)
    user_login = serializers.ReadOnlyField(source='user.login')
    article_id = serializers.ReadOnlyField(source='article.id')

    class Meta:
        depth = 1
        model = Comment
        fields = '__all__'

    def get_id(self, obj):
        return obj.id
