# Generated by Django 4.2.16 on 2024-11-19 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_profile_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={
                "ordering": ("user",),
                "verbose_name": "Профиль",
                "verbose_name_plural": "Профили",
            },
        ),
        migrations.AddField(
            model_name="profile",
            name="birth_date",
            field=models.DateField(blank=True, null=True, verbose_name="Дата рождения"),
        ),
        migrations.AddField(
            model_name="profile",
            name="slug",
            field=models.SlugField(
                blank=True, max_length=255, unique=True, verbose_name="URL"
            ),
        ),
    ]
