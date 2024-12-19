from django.conf import settings
from django.contrib.auth.views import (LoginView, LogoutView)
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import (CreateView)
from users.forms import (
    UserLoginForm,
    UserRegistrationForm)
from users.mixins import UserIsNotAuthenticated
from users.tasks import send_activate_email_message_task


class UserLoginView(UserIsNotAuthenticated, SuccessMessageMixin, LoginView):
    template_name = "users/auth/login.html"
    form_class = UserLoginForm
    success_message = "Добро пожаловать!"
    next_page = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация на сайте"
        return context

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            self.request.session.modified = True

        return super(UserLoginView, self).form_valid(form)


class UserRegistrationView(UserIsNotAuthenticated, SuccessMessageMixin, CreateView):
    template_name = "users/auth/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")
    success_message = "You have successfully registered"
    extra_context = {"title": "GameBlog - Registration"}

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_activate_email_message_task.delay(user.id)
        return redirect("users:email_confirmation_send")


class UserLogoutView(LogoutView):
    next_page = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "GameBlog - Logout"
        return context
