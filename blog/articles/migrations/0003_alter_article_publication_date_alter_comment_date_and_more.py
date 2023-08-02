# Generated by Django 4.2.2 on 2023-08-01 19:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 22, 3, 47, 184178), verbose_name='Article publication date'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 22, 3, 47, 185178), verbose_name='Comment date'),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(verbose_name='rating')),
                ('bookId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='articles.article')),
            ],
        ),
    ]