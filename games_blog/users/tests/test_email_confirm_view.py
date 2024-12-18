from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse_lazy


class BaseEmailConfirmViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.created_user = User.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='email@yahoo.com',
            password='<PASSWORD>',
        )
        cls.email_confirmation_send_url = reverse_lazy("users:email_confirmation_send")
        cls.email_confirmation_success_url = reverse_lazy("users:email_confirmation_success")
        cls.email_confirmation_failed_url = reverse_lazy("users:email_confirmation_failed")

    def generate_confirm_params(self):
        utoken = default_token_generator.make_token(self.created_user)
        uidb = urlsafe_base64_encode(force_bytes(self.created_user.pk))
        return {"uidb64": uidb, "token": utoken}


class EmailConfirmationSendViewTest(BaseEmailConfirmViewTest):

    def test_send_email_confirmation_message(self):
        response = self.client.get(self.email_confirmation_send_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/registration/email_confirmation_sent.html")

    def test_success_confirm_email_authenticated(self):
        confirm_email_url = reverse_lazy("users:confirm_email", kwargs=self.generate_confirm_params())
        response = self.client.get(confirm_email_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.email_confirmation_success_url)

    def test_failed_confirm_email_anonymous(self):
        confirm_email_url = reverse_lazy("users:confirm_email", kwargs={"uidb64": "uidb64", "token": "token"})
        response = self.client.get(confirm_email_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.email_confirmation_failed_url)
