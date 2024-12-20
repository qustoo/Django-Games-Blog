# Generated by Django 4.2.16 on 2024-11-25 17:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0018_rating_ip_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="publish",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Время публикации"
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="comment",
            name="name",
            field=models.CharField(max_length=15, verbose_name="Имя комментатора"),
        ),
        migrations.AlterField(
            model_name="comment",
            name="status",
            field=models.CharField(
                choices=[("PB", "Опубликовано"), ("DR", "Не опубликано")],
                default="PB",
                verbose_name="Статус комментария",
            ),
        ),
    ]
