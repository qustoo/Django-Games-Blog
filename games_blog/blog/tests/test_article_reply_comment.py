from rest_framework.reverse import reverse_lazy

from blog.models import Comment, Article
from django.test import TestCase
from blog.tests.test_data_mixin import SetUpCategory, SetUpUser


class ReplyArticleParentCommentViewTest(SetUpCategory, SetUpUser, TestCase):
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

        cls.parent_comment = Comment.objects.create(
            article=cls.article,
            author=cls.user,
            name=cls.user.username,
            email=cls.user.email,
            content="parent comment content",
        )
        cls.headers = {
            'X-Requested-With': 'XMLHttpRequest',
        }
        cls.url = reverse_lazy("blog:article_comment", kwargs={'slug': cls.article.slug})

    def test_reply_parent_comment_authenticated_user(self):
        self.client.force_login(self.user)
        child_comment_data = {
            "content": "child comment content",
            "parent": self.parent_comment.id,
        }

        response = self.client.post(path=self.url, data=child_comment_data, headers=self.headers)
        child_comment = Comment.objects.filter(content=child_comment_data['content']).first()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(child_comment.parent == self.parent_comment)
        self.assertTrue(child_comment.author == self.user)
        self.assertTrue(child_comment.name == self.user.username)
        self.assertTrue(child_comment.email == self.user.email)

    def test_reply_parent_comment_anonymous_user(self):
        child_comment_data = {
            "name": "testusername",
            "email": "testuser@mail.ru",
            "content": "child comment content",
            "parent": self.parent_comment.id,

        }

        response = self.client.post(path=self.url, data=child_comment_data, headers=self.headers)

        child_comment = Comment.objects.filter(content=child_comment_data['content']).first()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(child_comment.parent == self.parent_comment)
        self.assertTrue(child_comment.name == child_comment_data['name'])
        self.assertTrue(child_comment.email == child_comment_data['email'])
        self.assertTrue(child_comment.content == child_comment_data['content'])
