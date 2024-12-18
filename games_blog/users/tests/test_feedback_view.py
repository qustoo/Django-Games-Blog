from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch

from rest_framework.reverse import reverse_lazy

from blog.forms import FeedbackCreateForm
from blog.models import Feedback


class FeedbackViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@example.com'
        )
        FeedbackCreateForm.base_fields.pop('captcha', None)
        self.feedback_data = {
            "subject": "feedback subject",
            "content": "feedback content"
        }
        self.url = reverse_lazy("users:feedback")

    @patch('users.views.feedback_view.send_feedback_email_message_task.delay')
    @patch('users.views.feedback_view.get_client_ip')
    def test_send_feedback(self, mock_get_client_ip, mock_send_feedback_email):
        mock_get_client_ip.return_value = '127.0.0.1'
        mock_send_feedback_email.return_value = None
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.feedback_data)
        self.assertRedirects(response, reverse_lazy('home'), target_status_code=302)

        mock_send_feedback_email.assert_called_once()

        self.assertTrue(Feedback.objects.filter(ip_address='127.0.0.1').exists())
