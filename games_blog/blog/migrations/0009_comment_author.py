# Generated by Django 4.2.16 on 2024-11-19 14:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0008_remove_comment_user_article_views"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]