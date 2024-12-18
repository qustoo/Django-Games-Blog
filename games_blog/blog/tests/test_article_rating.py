import json

from blog.models import Article
from blog.tests.test_data_mixin import SetUpDatabaseTestData
from django.urls import reverse


def fetch_data_from_json_response(byte_str: bytes, *args):
    data_str = byte_str.decode("utf-8")
    data_dict = json.loads(data_str)
    return [data_dict[field] for field in args]


class CreateArticleViewTest(SetUpDatabaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("blog:rating")

    def test_rating_increase_decrease_authenticated_user(self):
        self.client.login(username="testuser", password="<PASSWORD>")

        # increase value for first time
        response = self.client.post(
            self.url, data={"article_id": self.article.id, "value": 1}
        )
        status, rate = fetch_data_from_json_response(
            response.content, "status", "rating_sum"
        )
        self.assertEqual(status, "created")
        self.assertEqual(rate, 1)

        # increase value for second time
        response = self.client.post(
            self.url, data={"article_id": self.article.id, "value": 1}
        )
        status, rate = fetch_data_from_json_response(
            response.content, "status", "rating_sum"
        )
        self.assertEqual(status, "deleted")
        self.assertEqual(rate, 1)

        # decrease value for first time
        response = self.client.post(
            self.url, data={"article_id": self.article.id, "value": -1}
        )
        status, rate = fetch_data_from_json_response(
            response.content, "status", "rating_sum"
        )
        self.assertEqual(status, "updated")
        self.assertEqual(rate, -1)

    def test_rating_increase_anonymous_user(self):

        response = self.client.post(
            self.url, data={"article_id": self.article.id, "value": 1}
        )
        self.assertEqual(response.content, b"You aren't authenticated")
        self.assertEqual(response.status_code, 403)
