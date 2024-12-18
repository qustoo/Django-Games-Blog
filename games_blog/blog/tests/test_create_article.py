from unittest.mock import patch

from django.utils import timezone

from blog.models import Article
from blog.tests.test_data_mixin import SetUpCategory, SetUpUser
from django.urls import reverse


class CreateArticleViewTest(SetUpCategory, SetUpUser):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("blog:articles_create")
        cls.valid_article_data = {
            "title": "Test Article Title",
            "category": cls.category.id,
            "full_description": "Test Article Description",
            "image": "posts/default_article.png",
            "publish": timezone.now(),
        }

    def test_create_article_login_required(self):
        response = self.client.post(self.url, data=self.valid_article_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login") + "?next=" + self.url)


    @patch('blog.views.crud_view.publish_article_scheduled.apply_async')
    def test_create_article_view_success(self, mocked_publish_article_scheduled):
        self.client.force_login(self.user)

        response = self.client.post(self.url, self.valid_article_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("blog:articles"))
        self.assertTrue(Article.objects.filter(title="Test Article Title").exists())
        mocked_publish_article_scheduled.assert_called_once()


        article = Article.objects.filter(title="Test Article Title").first()
        self.assertEqual(article.title, self.valid_article_data["title"])
        self.assertEqual(article.author, self.user)

    def test_create_article_view_failure(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "title", "Это поле обязательно для заполнения.")
        self.assertFormError(response, "form", "full_description", "Это поле обязательно для заполнения.")
        self.assertFormError(response, "form", "category", "Это поле обязательно для заполнения.")

