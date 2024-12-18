from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.reverse import reverse_lazy

from blog.forms import FeedbackCreateForm
from blog.models import Feedback
from django.contrib.messages.views import SuccessMessageMixin

from users.tasks import send_feedback_email_message_task
from django.views.generic import CreateView
from services.utils import get_client_ip


class FeedbackCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = "Письмо успешно отправлено!"
    template_name = "users/feedback/feedback.html"
    extra_context = {"title": "Контактная форма"}
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.ip_address = get_client_ip(self.request)
        feedback.user = self.request.user
        feedback.email = self.request.user
        send_feedback_email_message_task.delay(
            subject = feedback.subject,
            email = feedback.email,
            content = feedback.content,
            ip_address = feedback.ip_address,
            user_id = feedback.user.id,
        )
        return super().form_valid(form)
