from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

logger = get_task_logger(__name__)


User = get_user_model()


@shared_task(bind=True)
def send_active_email_message(self, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
    except Http404 as user_does_not_exist:
        logger.error(f"User with id {user_id} does not exist.")
        raise self.retry(exc=user_does_not_exist)

    current_site = Site.objects.get_current().domain
    token = default_token_generator.make_token(user)
    uidb = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy(
        "users:confirm_email", kwargs={"uidb64": uidb, "token": token}
    )
    subject = f"Активируйте свой аккаунт, {user.username}!"
    message = render_to_string(
        "users/email/activate_email_send.html",
        {
            "user": user,
            "activation_url": f"http://{current_site}{activation_url}",
        },
    )
    logger.info(
        f"Message for User with id {user_id} was successfully sent to {user.email}."
    )
    return user.email_user(subject, message)
