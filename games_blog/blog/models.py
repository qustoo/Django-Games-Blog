from datetime import date
from typing import Optional

from blog.managers import PublishedArticlesManager
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import FileExtensionValidator
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from services.utils import unique_slugify
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

SHORT_DESCRIPTION_MAX_LENGTH = 55


class Category(MPTTModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(verbose_name="URL", max_length=250, unique=True)
    description = models.TextField(verbose_name=_("Описание категории"), max_length=150)
    parent = TreeForeignKey(
        "self",
        verbose_name=_("Родительская категория"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ("title",)

    class MPTTMeta:
        order_insertion_by = ("title",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:articles_by_category", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

class Article(models.Model):
    class ArticleStatus(models.TextChoices):
        PUBLISHED = "PB", _("Опубликовано")
        NOT_PUBLISHED = "NP", _("Не опубликано")

    title = models.CharField(verbose_name=_("Заголовок"), max_length=200)
    slug = models.SlugField(
        verbose_name="URL",
        max_length=250,
        unique_for_date="publish",
        blank=True,
    )

    short_description = CKEditor5Field(
        verbose_name=_("Краткое описание"),
        max_length=SHORT_DESCRIPTION_MAX_LENGTH,
        blank=True,
        default="",
    )
    full_description = CKEditor5Field(
        verbose_name=_("Полное описание"),
    )
    image = models.ImageField(
        verbose_name=_("Превью поста"),
        upload_to="posts/%Y/%m/%d",
        default="posts/default_article.png",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    status = models.CharField(
        choices=ArticleStatus.choices,
        verbose_name=_("Статус публикации"),
        default=ArticleStatus.NOT_PUBLISHED,
        max_length=2,
    )
    author = models.ForeignKey(
        to=User,
        verbose_name=_("Автор"),
        on_delete=models.CASCADE,
        related_name="blog_articles",
    )
    updater = models.ForeignKey(
        to=User,
        verbose_name=_("Обновил"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="updater_posts",
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        related_name="articles",
        verbose_name=_("Категория"),
        on_delete=models.CASCADE,
    )
    publish = models.DateTimeField(
        verbose_name=_("Назначенное публикации"), default=timezone.now
    )
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedArticlesManager()  # конкретно-прикладной менеджер

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["-publish", "-created_at"])]
        verbose_name = _("Статья")
        verbose_name_plural = _("Статьи")
        default_manager_name = "published"

    def __str__(self):
        return f"{self.title} | {self.slug} | {self.status} | {self.short_description}"

    def get_absolute_url(self):
        return reverse(
            "blog:article_detail",
            kwargs={
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
                "slug": self.slug,
            },
        )

    def save(self, *args, **kwargs):
        self.pass_short_description()
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def pass_short_description(self):
        self.short_description = self.full_description[:SHORT_DESCRIPTION_MAX_LENGTH]

    def get_sum_rating(self):
        return sum([rating.value for rating in self.rating.all()])

    def get_view_count_per_date(self, certain_date: Optional[date]):
        if certain_date:
            return self.views.filter(viewed_on__date=certain_date).count()
        return self.views.count()

    def get_view_count(self):
        return self.get_view_count_per_date(certain_date=None)


class Rating(models.Model):
    article = models.ForeignKey(
        Article,
        verbose_name=_("Статья"),
        related_name="rating",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        verbose_name=_("Значение"), choices=[(1, _("Нравится")), (-1, _("Не нравится"))]
    )
    ip_address = models.GenericIPAddressField(verbose_name=_("IP Адрес"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("article", "user"),)
        verbose_name = _("Рейтинг")
        verbose_name_plural = _("Рейтинги")
        ordering = ("-created_at",)

    def __str__(self):
        return " | ".join([self.article.__str__(), f"Value is {self.value}"])


class Comment(MPTTModel):
    class CommentStatus(models.TextChoices):
        PUBLISHED = "PB", "Опубликовано"
        DRAFT = "DR", "Не опубликано"

    article = models.ForeignKey(
        Article, on_delete=models.PROTECT, related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
        blank=True,
    )
    name = models.CharField(verbose_name=_("Имя комментатора"), max_length=15)
    email = models.EmailField(verbose_name="Email")
    content = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    status = models.CharField(
        verbose_name=_("Статус комментария"),
        choices=CommentStatus.choices,
        default=CommentStatus.PUBLISHED,
    )
    level = models.IntegerField()
    parent = TreeForeignKey(
        "self",
        verbose_name=_("Родительский комментарий"),
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )

    class MTTMeta:
        order_insertion_by = ("-created_at",)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")

    def __str__(self):
        return f"Post by {self.author.username} on {self.article.slug}'"

    def created_status_ago(self):
        now = timezone.now()
        difference = now - self.created_at
        diff_days = difference.days
        if diff_days == 1:
            return str(diff_days) + " day ago"
        if diff_days < 30:
            return str(diff_days) + " days ago"


class Feedback(models.Model):
    subject = models.CharField(max_length=255, verbose_name=_("Тема письма"))
    email = models.EmailField(
        max_length=255, verbose_name=_("Электронный адрес (email)")
    )
    content = CKEditor5Field(verbose_name=_("Содержимое письма"))
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата отправки")
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP отправителя"), blank=True, null=True
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Обратная связь")
        verbose_name_plural = _("Обратная связь")
        ordering = ["-time_create"]
        db_table = "app_feedback"

    def __str__(self):
        return f"Вам письмо от {self.email}"


class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="views")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    viewed_on = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")

    class Meta:
        ordering = ("-viewed_on",)
        indexes = [models.Index(fields=["-viewed_on"])]
        verbose_name = "Просмотр"
        verbose_name_plural = "Просмотры"

    def __str__(self):
        return self.article.slug
