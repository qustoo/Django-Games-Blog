from django.db import transaction, connection

from blog.models import Category, Article
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from services.utils import unique_slugify

User = get_user_model()

class SetUpCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.category = Category.objects.create(
            title="Category Title",
            slug="category",
            description="Category Description",
        )


class SetUpUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if User.objects.filter(username="testuser").exists():
            cls.user = User.objects.get(username="testuser")
        else:
            cls.user = User.objects.create_user(
                username="testuser", email="<EMAIL>", password="<PASSWORD>"
            )


class SetUpDatabaseTestData(SetUpCategory, SetUpUser):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.article = Article.objects.create(
            title="Test Article",
            full_description="This is a description of an articles.",
            author=cls.user,
            status="PB",
            category=cls.category,
            tags="jazz, dance",
        )



def create_articles(n, user, category):
    articles = []
    for i in range(n):
        article = Article(
            title=f"Article #{i + 1}",
            full_description=f"Total Description  for #{i + 1} article",
            status="PB",
            publish=timezone.now(),
            category=category,
            author=user,
        )
        if not article.slug:
            article.slug = unique_slugify(article, article.title)
        articles.append(article)

    with transaction.atomic():
        Article.objects.bulk_create(articles)

    return articles
