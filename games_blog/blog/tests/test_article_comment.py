from blog.tests.test_data_mixin import SetUpDatabaseTestData
from django.urls import reverse


class CreateArticleCommentViewTest(SetUpDatabaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("blog:article_comment", kwargs={"slug": cls.article.slug})

    def test_create_comment_not_authenticated_user(self):
        comment_data = {
            "name": "Ivan",
            "email": "ivan@mail.ru",
            "content": "comment content",
        }
        response = self.client.post(self.url, comment_data)
        self.assertRedirects(response, self.article.get_absolute_url())

        self.article.refresh_from_db()
        comments = self.article.comments.all().count()
        self.assertEqual(comments, 1)

        response = self.client.get(self.article.get_absolute_url())
        self.assertContains(response, comment_data["name"])
        self.assertContains(response, comment_data["content"])

    def test_create_comment_authenticated_user(self):
        self.client.login(username="testuser", password="<PASSWORD>")
        comment_data = {
            "content": "comment content",
        }

        response = self.client.post(self.url, comment_data)
        self.assertRedirects(response, self.article.get_absolute_url())

        self.article.refresh_from_db()
        comments = self.article.comments.filter(author=self.user)
        self.assertEqual(comments.count(), 1)

        self.assertEqual(comments[0].content, "comment content")
        self.assertEqual(comments[0].author, self.user)
        self.assertEqual(comments[0].email, self.user.email)
        self.assertEqual(comments[0].status, "PB")

    def test_create_comment_invalid_data(self):
        comment_data = {}
        response = self.client.post(self.url, comment_data)
        self.assertRedirects(response, self.article.get_absolute_url())
        comments = self.article.comments.all()
        self.assertEqual(comments.count(), 0)

    def test_create_comment_guest_and_authenticated_user(self):
        self.client.login(username="testuser", password="<PASSWORD>")

        comment_data = {
            "name": "some name",
            "email": "email@com.ru",
            "content": "comment content",
        }

        response_login_user = self.client.post(
            self.url, data={"content": comment_data["content"]}
        )

        self.assertRedirects(response_login_user, self.article.get_absolute_url())
        self.article.refresh_from_db()

        comments = self.article.comments.all()

        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments[0].content, "comment content")
        self.assertEqual(comments[0].author, self.user)
        self.assertEqual(comments[0].name, self.user.username)
        self.assertEqual(comments[0].email, self.user.email)
        self.assertEqual(comments[0].status, "PB")

        self.client.logout()

        response_guest_user = self.client.post(self.url, comment_data)

        self.assertRedirects(response_guest_user, self.article.get_absolute_url())
        self.article.refresh_from_db()

        comments = self.article.comments.all()

        self.assertEqual(comments.count(), 2)
        self.assertEqual(comments[1].content, "comment content")
        self.assertEqual(comments[1].name, comment_data["name"])
        self.assertEqual(comments[1].email, comment_data["email"])
        self.assertEqual(comments[1].status, "PB")

    # def test_create_create_comment_parent_and_child(self):
    #     self.client.login(username="testuser", password="<PASSWORD>")
    #     parent_comment_data = {"content": "parent comment content"}
    #     child_comment_data = {"content": "child comment content"}
    #     parent_response_json = self.client.post(
    #         self.url, parent_comment_data
    #     )
    #     self.assertRedirects(parent_response_json, self.article.get_absolute_url())
    #
    #     # доп логика на обработку как подкоментарий
    #     child_response_json = self.client.post(
    #         self.url, child_comment_data
    #     )
    #     self.assertRedirects(child_response_json, self.article.get_absolute_url())
    #
    #     # Refresh article
    #     self.article.refresh_from_db()
    #
    #
    #     comments = self.article.comments.all()
    #     parent_comment = comments.filter(content=parent_comment_data['content'])[0]
    #     child_comment = comments.filter(content=child_comment_data['content'])[0]
    #     print(child_comment.parent_id)
    #     # self.assertEqual(child_comment.parent, parent_comment)
