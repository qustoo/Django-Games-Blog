# Generated by Django 4.2.16 on 2024-11-21 14:50

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_profile_avatar_alter_profile_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name="Биография"),
        ),
    ]
