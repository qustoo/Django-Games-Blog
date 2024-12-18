
from blog.models import Article
from django.urls import reverse

from games_blog.settings import PAGINATE_BY
from .test_data_mixin import SetUpCategory, SetUpUser, create_articles


class GetArticlesByCategoryTest(SetUpCategory, SetUpUser):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.article_per_page = PAGINATE_BY
        cls.article_numbers = 10
        cls.articles = create_articles(
            n=cls.article_numbers, user=cls.user, category=cls.category
        )
        cls.url = reverse(
            "blog:articles_by_category", kwargs={"slug": cls.category.slug}
        )

    def test_get_count_articles_by_category(self):
        articles = Article.published.filter(category=self.category).count()
        self.assertEqual(articles, self.article_numbers)

    def test_articles_by_category_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertTemplateUsed(response, "blog/articles/articles.html")
        self.assertEqual(len(response.context["articles"]), self.article_per_page)

    def test_articles_by_category_invalid_slug(self):
        response = self.client.get(
            reverse("blog:articles_by_category", kwargs={"slug":"invalid-slug"})
        )
        self.assertEqual(response.status_code, 404)
