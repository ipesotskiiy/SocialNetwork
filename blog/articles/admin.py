from django.contrib import admin
from articles.models import Article, Comment, Genre, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'average_rate', 'publication_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('date',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

