# Generated by Django 4.2.16 on 2024-11-13 23:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "Статья",
                "verbose_name_plural": "Статьи",
            },
        ),
        migrations.AddField(
            model_name="article",
            name="publish",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="article",
            name="status",
            field=models.CharField(
                choices=[
                    ("PB", "Опубликовано"),
                    ("NP", "Не опубликано"),
                    ("PR", "В работе"),
                ],
                default="PB",
                max_length=2,
                verbose_name="Статус публикации",
            ),
        ),
        migrations.AddIndex(
            model_name="article",
            index=models.Index(
                fields=["-publish"], name="blog_articl_publish_2a54df_idx"
            ),
        ),
    ]
