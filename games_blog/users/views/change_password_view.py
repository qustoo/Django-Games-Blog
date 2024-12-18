from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy

from users.forms import UserPasswordChangeForm



class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = "users/password/change_password.html"
    success_message = "Пароль успешно изменен!"
    form_class = UserPasswordChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменение пароля на сайте"
        return context

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_detail", kwargs={"slug": self.request.user.profile.slug}
        )
