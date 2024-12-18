from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse_lazy

from users.forms import UserPasswordResetForm

RESET_PASSWORD_MESSAGE = """
На ваш адрес электронной почты было отправлено письмо со ссылкой для сброса пароля. Пожалуйста, проверьте свою почту.
Если вы не получили письмо, проверьте папку "Спам" или попробуйте снова.
"""


class ResetPasswordViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Delete captcha
        UserPasswordResetForm.base_fields.pop('captcha', None)

        cls.created_user = User.objects.create_user(
            username='testuser',
            email='testuser@mail.ru',
            password='<PASSWORD>'
        )
        cls.password_reset_url = reverse_lazy("users:password_reset")
        cls.password_reset_done_url = reverse_lazy("users:password_reset_done")
        cls.password_reset_complete_url = reverse_lazy("users:password_reset_complete")

        cls.uidb64 = urlsafe_base64_encode(force_bytes(cls.created_user.pk))
        cls.token = default_token_generator.make_token(cls.created_user)
        cls.password_reset_confirm_url = reverse_lazy(
            'users:password_reset_confirm',
            kwargs={'uidb64': cls.uidb64, 'token': cls.token}
        )

    # Запрос на восставление пароля
    def test_password_reset_view(self):
        response = self.client.post(self.password_reset_url, {"email": self.created_user.email})
        self.assertTemplateUsed(response, "users/email/password_reset_email.html")
        self.assertRedirects(response, self.password_reset_done_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Письмо с инструкцией по восстановлению пароля отправлена на ваш email")

    # Форма для ввода нового пароля
    def test_password_reset_confirm_view_success(self):
        response = self.client.post(self.password_reset_confirm_url,
                                    {'new_password1': '<PASSWORD>', 'new_password2': '<PASSWORD>'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/users/reset/{}/set-password/".format(self.uidb64))

    def test_password_reset_complete_view(self):
        response = self.client.get(self.password_reset_complete_url)
        self.assertTemplateUsed(response, "users/password/password_reset_complete.html")
        self.assertContains(response, "Ваш пароль был успешно изменен. Теперь вы можете войти в свою учетную запись.")
