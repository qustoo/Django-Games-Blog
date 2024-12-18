from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from services.email import send_active_email_message

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_verification_email_task(self, user_id):
    try:
        user = User.objects.get(pk=user_id)
        send_mail(
            "Verify your  account",
            "Follow this link to verify your account: "
            "http://localhost:8000/verify/%s" % user.username,
            "admin@localhost.ru",
            [user.email],
            fail_silently=False,
        )
        logger.info("Verification email sent")
    except User.DoesNotExist as user_does_not_exist:
        logger.error(f"User with id {user_id} does not exist.")
        raise self.retry(exc=user_does_not_exist)


@shared_task(max_retries=3, default_retry_delay=10)
def send_activate_email_message_task(user_id):
    return send_active_email_message(user_id)


@shared_task(name="send_feedback_email_message_task", max_retries=3, default_retry_delay=10)
def send_feedback_email_message_task(subject, email, content, ip_address, user_id):
    user = get_object_or_404(User, id=user_id)
    message_data = render_to_string(
        "users/email/feedback_email_send.html",
        {"email": email, "content": content, "ip_address": ip_address, "user": user},
    )
    email = EmailMessage(
        subject=subject,
        body=message_data,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    email.send(fail_silently=False)
