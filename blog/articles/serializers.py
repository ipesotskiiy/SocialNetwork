from datetime import datetime

from rest_framework import serializers
from django.db import transaction

from articles.models import Article, Genre, Comment, Rating, Like, Dislike, Tag


class RatingSerializer(serializers.ModelSerializer):
    """
    Сериализатор рейтинга
    """
    user_id = serializers.ReadOnlyField(source='user.id')
    article_id = serializers.ReadOnlyField(source='article.id')
    rating = serializers.IntegerField()

    def validate(self, attrs):
        """
        Валидация которая нужна для того, что бы рейтинг был не выше 5
        """
        if attrs['rating'] > 5:
            attrs['rating'] = 5
        return attrs

    class Meta:
        model = Rating
        fields = (
            '__all__'
        )


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    class Meta:
        model = Genre
        fields = (
            '__all__'
        )


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор тегоа
    """
    articles = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """
    Сериализатор статей
    """
    login = serializers.ReadOnlyField(source='user.login')
    publication_date = serializers.DateTimeField(default=datetime.now(), read_only=True)
    average_rate = serializers.SerializerMethodField('calculate_average_rate', read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        depth = 1
        model = Article
        fields = '__all__'

    def calculate_average_rate(self, obj):
        """
        Функция для высчитывания среднего рейтинга статьи и держащая его в пределах от 0 до 5
        """
        ratings = [i.get('rating') for i in RatingSerializer(obj.ratings, many=True).data]
        len_rat = len(ratings)
        sum_rat = sum(ratings)

        if len_rat == 0 or sum_rat == 0:
            return 0

        average_rate = sum_rat / len_rat

        if average_rate > 5:
            average_rate = 5

        obj.average_rate = round(average_rate, 1)
        obj.save()
        return round(average_rate, 1)

    def create(self, validated_data):
        genre_names = validated_data.pop('genres', [])
        tag_names = validated_data.pop('tags', [])
        user = validated_data.get('user_id')

        with transaction.atomic():
            article = Article.objects.create(**validated_data)

            for genre_name in genre_names:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                article.genres.add(genre)

            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                article.tags.add(tag)

            user.count_article += 1
            user.save()

        return article


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор комментариев
    """
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


class LikeSerializer(serializers.ModelSerializer):
    """
    Сериализатор лайков
    """

    class Meta:
        model = Like
        fields = '__all__'


class DislikeSerializer(serializers.ModelSerializer):
    """
    Сериализатор дизлайков
    """

    class Meta:
        model = Dislike
        fields = '__all__'
