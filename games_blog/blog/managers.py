from django.db import models


class PublishedArticlesManager(models.Manager):

    def not_published(self):
        return (
            self.get_queryset()
            .filter(status="NB")
            .select_related("category", "author")
            .order_by("-publish")
        )

    def all(self):
        return (
            self.get_queryset()
            .filter(status="PB")
            .select_related("category", "author")
            .order_by("-publish")
        )

    def detail(self, article_slug):
        return (
            self.get_queryset()
            .filter(slug=article_slug, status="PB")
            .select_related("author", "category")
            .prefetch_related(
                "comments", "comments__author", "comments__author__profile"
            )
        )
