# Generated by Django 4.2.16 on 2024-11-20 13:09

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0010_article_short_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.AddField(
            model_name="comment",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="blog.comment",
                verbose_name="Родительский комментарий",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="status",
            field=models.CharField(
                choices=[("PB", "Опубликовано"), ("DR", "Не опубликано")], default="PB"
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=models.SlugField(
                blank=True,
                max_length=250,
                unique=True,
                unique_for_date="publish",
                verbose_name="URL",
            ),
        ),
    ]