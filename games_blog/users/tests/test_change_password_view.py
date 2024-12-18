from django.contrib.messages import get_messages
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.reverse import reverse_lazy

from users.forms import UserPasswordChangeForm


class ChangePasswordViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_user = User.objects.create_user(
            username="testuser",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        cls.user_password = "<PASSWORD>"
        cls.change_password_url = reverse_lazy("users:password_change")

    def test_change_password_success(self):
        self.client.force_login(self.create_user)
        new_user_password = self.user_password + "NEW"
        new_password_data = {
            'old_password': self.user_password,
            'new_password1': new_user_password,
            'new_password2': new_user_password,
        }
        response = self.client.post(self.change_password_url, new_password_data)
        self.assertRedirects(response, reverse_lazy("users:profile_detail", kwargs={"slug": self.create_user.profile.slug}))
        self.create_user.refresh_from_db()
        self.assertTrue(self.create_user.check_password(new_user_password))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Пароль успешно изменен!")

    def test_change_password_wrong_old_password(self):
        self.client.force_login(self.create_user)
        response = self.client.post(self.change_password_url, {"old_password": "wrongpassword", "new_password1": "<PASSWORD>", "new_password2": "<PASSWORD>"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ваш старый пароль введен неправильно. Пожалуйста, введите его снова.")


    def test_change_password_passwords_different(self):
        self.client.force_login(self.create_user)
        response = self.client.post(self.change_password_url, {"old_password": self.user_password, "new_password1": "<PASSWORD>", "new_password2": "<PASSWORD>123"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Введенные пароли не совпадают.")
