from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class UserIsNotAuthenticated(UserPassesTestMixin):
    def test_func(self):
        if any([self.request.user.is_authenticated, self.request.user.is_staff]):
            messages.info(
                self.request, "Вы уже авторизованы и не можете посетить эту страницу."
            )
            return False
        return True

    def handle_no_permission(self):
        return redirect("home")
