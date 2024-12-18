# Generated by Django 4.2.16 on 2024-11-21 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0014_remove_article_blog_articl_publish_2a54df_idx_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=models.SlugField(
                blank=True,
                max_length=250,
                unique_for_date="publish",
                verbose_name="URL",
            ),
        ),
    ]