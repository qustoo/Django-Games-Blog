from rest_framework.reverse import reverse_lazy
from django.db import connection
from .test_data_mixin import SetUpCategory, SetUpUser
from blog.models import Article


class SearchArticlesTest(SetUpCategory, SetUpUser, ):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.article = Article.objects.create(
            title="jazz article",
            full_description="This is a description of jazz/dance article.",
            author=cls.user,
            status="PB",
            category=cls.category,
            tags="jazz, dance",
        )
        cls.url = reverse_lazy("blog:search")

        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    @classmethod
    def tearDownClass(cls):
        with connection.cursor() as cursor:
            cursor.execute("DROP EXTENSION IF EXISTS pg_trgm;")

    def test_search_articles(self):
        response = self.client.get(self.url, {"query": "jazz article"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["articles"], Article.published.filter(pk=self.article.id))

        # Article data
        self.assertContains(response, self.article.title)
        self.assertContains(response, self.article.full_description)
        self.assertContains(response, self.article.author)
        self.assertContains(response, self.article.category)

        for tag in self.article.tags.split(','):
            self.assertContains(response, tag.strip())

    def test_search_articles_no_results(self):
        response = self.client.get(self.url, {"query": "notexistsdata"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)
        self.assertEqual(len(response.context["articles"]), 0)

    def test_search_articles_without_empty(self):
        response = self.client.get(self.url, {"query": ""})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['articles'], Article.published.all())
