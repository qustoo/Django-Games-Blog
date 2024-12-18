from blog.models import Article
from blog.tests.test_data_mixin import SetUpDatabaseTestData
from django.urls import reverse


class DeleteArticleViewTest(SetUpDatabaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("blog:articles_delete", kwargs={"slug": cls.article.slug})

    def test_delete_article_view_authenticated_user(self):
        self.client.login(username="testuser", password="<PASSWORD>")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        articles = Article.objects.all()
        self.assertEqual(articles.count(), 0)

    def test_delete_article_view_anonymous_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login") + "?next=" + self.url)

        articles = Article.objects.all()
        self.assertNotEquals(articles.count(), 0)

    def test_context_data(self):
        self.client.login(username="testuser", password="<PASSWORD>")
        response = self.client.get(self.url)
        self.assertEqual(
            response.context["title"], f"Удаление статьи: {self.article.title}"
        )
