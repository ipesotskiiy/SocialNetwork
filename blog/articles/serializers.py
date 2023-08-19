from datetime import datetime

from rest_framework import serializers

from articles.models import Article, Genre, Comment, Rating, Like, Dislike
from users.models import User


class RatingSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    rating = serializers.IntegerField()

    def validate(self, attrs):
        if attrs['rating'] > 5:
            attrs['rating'] = 5
        elif attrs['rating'] < 0:
            attrs['rating'] = 0
        return attrs

    class Meta:
        model = Rating
        fields = (
            '__all__'
        )


class ArticleSerializer(serializers.ModelSerializer):
    article_id = serializers.SerializerMethodField('get_id')
    login = serializers.ReadOnlyField(source='user.login')
    publication_date = serializers.DateTimeField(default=datetime.now(), read_only=True)
    average_rate = serializers.SerializerMethodField('calculate_average_rate', default=0.0, read_only=True)
    count_like = serializers.IntegerField(default=0, read_only=True)
    count_dislike = serializers.IntegerField(default=0, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        depth = 1
        model = Article
        fields = (
            '__all__'
        )

    def get_id(self, obj):
        return obj.id

    def calculate_average_rate(self, obj):
        ratings = [i.get('rating') for i in RatingSerializer(obj.ratings, many=True).data]
        len_rat = len(ratings)
        sum_rat = sum(ratings)

        if len_rat == 0 or sum_rat == 0:
            return 0

        average_rate = sum_rat / len_rat

        if average_rate > 5:
            average_rate = 5
        round_average_rate = round(average_rate, 1)
        return round_average_rate


class GenreSerializer(serializers.ModelSerializer):
    genre_id = serializers.SerializerMethodField('get_id')

    class Meta:
        model = Genre
        fields = ('name',
                  'genre_id')


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.SerializerMethodField('get_id')
    date = serializers.DateTimeField(required=False, default=datetime.now(), format="%Y-%m-%d %H:%M:%S", read_only=True)
    user_login = serializers.ReadOnlyField(source='user.login')
    article_id = serializers.ReadOnlyField(source='article.id')
    liked_by = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        depth = 1
        model = Comment
        fields = '__all__'

    def update(self, instance, validated_data):
        liked_by = validated_data.pop('liked_by')
        for i in liked_by:
            instance.liked_by.add(i)
        instance.save()
        return instance

    def get_id(self, obj):
        return obj.id


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = '__all__'
