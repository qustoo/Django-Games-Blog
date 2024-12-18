from django.utils import timezone
from django.urls import reverse
from .test_data_mixin import SetUpDatabaseTestData
from blog.models import Category, Article

class UpdateArticleViewTest(SetUpDatabaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.valid_form_data = {
            "title": "Updated Article title",
            "full_description": "Updated Full Description",
            "category": cls.category.id,
            "image": "posts/default_article.png",
            "status": "PB",
            "tags": cls.article.tags,
            "updater":cls.user,
            "views": 1,
            "publish": timezone.now(),
        }
        cls.url = reverse("blog:articles_update", kwargs={"slug": cls.article.slug})

    def test_article_update_view_success(self):
        self.client.login(username="testuser", password="<PASSWORD>")

        response = self.client.post(self.url, data=self.valid_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("blog:articles"))

        self.article.refresh_from_db()

        self.assertEqual(self.article.title, self.valid_form_data["title"])
        self.assertEqual(self.article.full_description, self.valid_form_data["full_description"])
        self.assertEqual(self.article.status, self.valid_form_data["status"])
        self.assertEqual(self.article.updater, self.user)

    def test_article_update_view_invalid_form(self):
        self.client.login(username="testuser", password="<PASSWORD>")
        response = self.client.post(self.url, {})
        # invalid update
        self.assertEqual(response.status_code, 200)

    def test_article_update_view_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login") + "?next=" + self.url)

    def test_update_context_data(self):
        self.client.login(username="testuser", password="<PASSWORD>")
        response = self.client.get(self.url)
        self.assertEqual(
            response.context["title"], f"Обновление статьи: {self.article.title}"
        )
