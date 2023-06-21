from datetime import datetime

from django.db import models

# Create your models here.
from users.models import User


class Article(models.Model):
    tag_id = models.ManyToManyField('Tag')
    genre_id = models.ManyToManyField('Genre')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Article name', max_length=40)
    text = models.TextField(verbose_name='Article text', max_length=100000)
    average_rate = models.FloatField(verbose_name='Article average rate', null=True, blank=True)
    publication_date = models.DateTimeField(verbose_name='Article publication date')
    count_like = models.PositiveIntegerField(verbose_name="Article count like", default=0)
    count_dislike = models.PositiveIntegerField(verbose_name='Article count dislike', default=0)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.name


class Comment(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Comment text', max_length=200)
    date = models.DateTimeField(verbose_name='Comment date', default=datetime.now())
    count_like = models.PositiveIntegerField(default=0)
    count_dislike = models.PositiveIntegerField(default=0)

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
