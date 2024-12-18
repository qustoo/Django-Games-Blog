
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View, TemplateView

from django.contrib.auth.models import User


class EmailConfirmationSendView(TemplateView):
    template_name = "users/registration/email_confirmation_sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено"
        return context


class EmailConfirmationSuccessView(TemplateView):
    template_name = "users/registration/email_confirmation_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес активирован"
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = "users/registration/email_confirmation_failed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес не активирован"
        return context



class ConfirmUserEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist, OverflowError):
            user = None
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("users:email_confirmation_success")
        else:
            return redirect("users:email_confirmation_failed")


