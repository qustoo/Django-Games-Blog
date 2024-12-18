from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse_lazy
from unittest.mock import patch
from users.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User


class UserLoginViewTest(TestCase):
    def setUp(self):
        UserLoginForm.base_fields.pop('captcha', None)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@example.com'
        )
        self.url = reverse_lazy('users:login')

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/auth/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpassword123',
            'remember_me': True})
        # self.assertRedirects(response, reverse_lazy('home'), target_status_code=302)

    def test_login_view_post_invalid(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'wrongpassword',
            'remember_me': True,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. ')


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'email@email.com',
            'password1': '/4D{ne}dMt>2q($z',
            'password2': '/4D{ne}dMt>2q($z',
            'username': 'johndoe',
        }
        self.url = reverse_lazy('users:registration')
        self.redirect_url = reverse_lazy('users:email_confirmation_send')

    def is_valid_form(self):
        UserRegistrationForm.base_fields.pop('captcha', None)
        form = UserRegistrationForm(data=self.user_data)
        return form

    def test_registration_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/auth/register.html')

    @patch('users.views.auth_views.send_activate_email_message_task.delay')
    def test_register_and_activate_user_post_valid(self, mock_send_email):
        UserRegistrationForm.base_fields.pop('captcha', None)
        response = self.client.post(self.url, data=self.user_data)

        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(User.objects.count(), 1)

        created_user = User.objects.get(username='johndoe')
        self.assertFalse(created_user.is_active)
        self.assertEqual(created_user.first_name, self.user_data['first_name'])
        self.assertEqual(created_user.last_name, self.user_data['last_name'])
        self.assertEqual(created_user.username, self.user_data['username'])
        self.assertEqual(created_user.email, self.user_data['email'])

        mock_send_email.assert_called_once_with(created_user.id)

        token = default_token_generator.make_token(created_user)
        uidb = urlsafe_base64_encode(force_bytes(created_user.pk))
        self.client.get(
            path=reverse_lazy("users:confirm_email", kwargs={'uidb64': uidb, 'token': token})
        )
        created_user.refresh_from_db()
        self.assertTrue(created_user.is_active)

    @patch('users.views.auth_views.send_activate_email_message_task.delay')
    def test_register_and_activate_user_post_invalid(self, mock_send_email):
        UserRegistrationForm.base_fields.pop('captcha', None)
        self.user_data['password1'] = '/4D{ne}dMt>2q($z'
        self.user_data['password2'] = '/4D{ne}'
        response = self.client.post(self.url, data=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/auth/register.html')



class UserLogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@example.com'
        )
        self.url = reverse_lazy('users:logout')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse_lazy('home'), target_status_code=302)

    def test_logout_view_get_context(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
