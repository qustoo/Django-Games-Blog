from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy

from users.forms import UserPasswordResetForm, UserSetNewPasswordForm


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = "users/password/password_reset.html"
    # Перенаправление на страницу где сказано что письмо отправлено
    success_url = reverse_lazy("users:password_reset_done")
    success_message = (
        "Письмо с инструкцией по восстановлению пароля отправлена на ваш email"
    )
    subject_template_name = "users/email/password_subject_reset_mail.txt"
    email_template_name = "users/email/password_reset_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "GameBlog - Сброс пароля"
        return context

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password/password_reset_done.html"



class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = UserSetNewPasswordForm
    template_name = "users/password/password_reset_confirm.html"
    success_message = ("Пароль успешно изменен. Можете авторизоваться на сайте.")

    def get_success_url(self):
        return reverse_lazy("users:password_reset_complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пароль успешно сброшен"
        return context


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password/password_reset_complete.html"
    extra_context = {"title": "GameBlog - Пароль успешно изменен"}
