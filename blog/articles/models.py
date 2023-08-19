from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User


class Article(models.Model):
    tag_id = models.ManyToManyField('Tag')
    genre_id = models.ManyToManyField('Genre')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Article name', max_length=40)
    text = models.TextField(verbose_name='Article text', max_length=100000)
    average_rate = models.FloatField(verbose_name='Article average rate', null=True, blank=True, default=0.0)
    publication_date = models.DateTimeField(verbose_name='Article publication date', default=datetime.now())

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.name


class Comment(models.Model):
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
    name = models.CharField()

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(verbose_name='rating', validators=[MaxValueValidator(5)], default=0)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return str(self.rating)


class Like(models.Model):
    user_id = models.ManyToManyField(User)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='like_comment')


class Dislike(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_dislike = models.BooleanField(default=False)
    dislike_date = models.DateTimeField(default=datetime.now())