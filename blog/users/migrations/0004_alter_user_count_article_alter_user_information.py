# Generated by Django 4.2.2 on 2023-06-13 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers_user_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='count_article',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Count articles'),
        ),
        migrations.AlterField(
            model_name='user',
            name='information',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Information about yourself'),
        ),
    ]