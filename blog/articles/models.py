from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User


class Article(models.Model):
    """
    Модель статей
    """

    tags = models.ManyToManyField('Tag', related_name='tags')
    genres = models.ManyToManyField('Genre')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(verbose_name='Article name', max_length=40)
    text = models.TextField(verbose_name='Article text', max_length=100000)
    average_rate = models.FloatField(verbose_name='Article average rate', null=True, blank=True, default=0.0)
    publication_date = models.DateTimeField(verbose_name='Article publication date', default=datetime.now())

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Модель комментариев
    """

    article_id = models.ForeignKey(Article, related_name='comment', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Comment text', max_length=200)
    date = models.DateTimeField(verbose_name='Comment date', default=datetime.now())

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text


class Genre(models.Model):
    """
    Модель жанров
    """
    GENRES = (
        ('Хоррор', 'Хоррор'),
        ('Фентези', 'Фентези'),
        ('Научная фантастика', 'Научная фантастика'),
        ('Для детей', 'Для детей'),
    )

    name = models.CharField("Genre name", max_length=100, choices=GENRES)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Модель тегов
    """

    name = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Rating(models.Model):
    """
    Модель рейтинга статей
    """

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(verbose_name='rating', validators=[MaxValueValidator(5)], default=0)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return str(self.rating)


class Like(models.Model):
    """
    Модель лайков коммнтариеев
    """

    user_id = models.ManyToManyField(User)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='like_comment')


class Dislike(models.Model):
    """
    Модель дизлайка комментариев
    """
    user_id = models.ManyToManyField(User)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='dislike_comment')