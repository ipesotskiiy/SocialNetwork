# Generated by Django 4.2.2 on 2023-06-21 15:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_alter_comment_count_dislike_alter_comment_count_like_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='count_dislike',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='count_like',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 21, 18, 46, 12, 391783), verbose_name='Comment date'),
        ),
    ]