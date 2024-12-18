from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils import timezone

from services.utils import unique_slugify


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    slug = models.SlugField(verbose_name="URL", max_length=255, blank=True)
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="profile/avatars/%Y/%m/%d",
        default="profile/avatars/default.jpg",
    )

    bio = CKEditor5Field(config_name="awesome_ckeditor", verbose_name="Биография")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    def __str__(self):
        return self.user.username

    class Meta:
        """
        Сортировка, название таблицы в базе данных
        """

        ordering = ("user",)
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        self.slug = self.user.username
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse("users:profile_detail", kwargs={"slug": self.slug})

    def is_online(self):
        last_seen = cache.get(f"last_seen-{self.user.id}")
        return last_seen and timezone.now() < last_seen + timezone.timedelta(minutes=5)
