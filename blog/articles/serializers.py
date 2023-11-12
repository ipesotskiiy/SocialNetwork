from datetime import datetime

from rest_framework import serializers

from articles.models import Article, Genre, Comment, Rating, Like, Dislike


class RatingSerializer(serializers.ModelSerializer):
    """
    Сериализатор рейтинга
    """
    user_id = serializers.ReadOnlyField(source='user.id')
    rating = serializers.IntegerField()

    def validate(self, attrs):
        """
        Валидация которая нужна для того, что бы рейтинг был не выше 5 и не ниже 0
        """
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


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    # name = serializers.ChoiceField(choices=Genre.GENRES)

    class Meta:
        model = Genre
        fields = (
            '__all__'
        )


class ArticleSerializer(serializers.ModelSerializer):
    """
    Сериализатор статей
    """
    # article_id = serializers.SerializerMethodField('get_id')
    login = serializers.ReadOnlyField(source='user.login')
    publication_date = serializers.DateTimeField(default=datetime.now(), read_only=True)
    average_rate = serializers.SerializerMethodField('calculate_average_rate', default=0.0, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True)

    class Meta:
        depth = 1
        model = Article
        fields = '__all__'

    # def get_id(self, obj):
    #     return obj.id

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
        round_average_rate = round(average_rate, 1)
        return round_average_rate

    def create(self, validated_data):
        title = validated_data.get('title')
        text = validated_data.get('text')
        genre_names = validated_data.get('genres', [])  # Получаем выбранные жанры в виде списка имен

        article = Article.objects.create(title=title, text=text, user_id=validated_data['user_id'])

        for genre_name in genre_names:
            genre, _ = Genre.objects.get_or_create(name=genre_name)  # Получаем или создаем жанр
            article.genres.add(genre)  # Связываем жанр со статьей

        return article
        # author_data = validated_data.pop('genre_id')
        # genre_serializer = GenreSerializer(data=author_data)
        # genre = genre_serializer.save()

        # if genre_serializer.is_valid():
        #
        # else:
        #     raise serializers.ValidationError('Error creating author')
        # genre = Genre.objects.create(name=author_data.get('name'))

        # book = Article.objects.create(genre_id=genre, **validated_data)
        # return book


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
