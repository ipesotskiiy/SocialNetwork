from django.db import models

# Create your models here.
from users.models import User


class Article(models.Model):
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)
    genre_id = models.ManyToManyField('Genre')
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Article name', max_length=40)
    text = models.TextField(verbose_name='Article text', max_length=100000)
    average_rate = models.FloatField(verbose_name='Article average rate')
    publication_date = models.DateTimeField(verbose_name='Article publication date')
    count_like = models.PositiveIntegerField(verbose_name="Article count like", default=0)
    count_dislike = models.PositiveIntegerField(verbose_name='Article count dislike', default=0)


class Comment(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Comment text', max_length=200)
    date = models.DateTimeField()
    count_like = models.PositiveIntegerField()
    count_dislike = models.PositiveIntegerField()


class Genre(models.Model):
    name = models.CharField()


class Tag(models.Model):
    name = models.CharField(max_length=20)
