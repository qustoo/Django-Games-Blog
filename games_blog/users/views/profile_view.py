from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect

from django.urls import reverse_lazy, reverse

from django.views.generic import (DetailView,
                                  UpdateView, )

from games_blog import settings
from users.forms import (ProfileUpdateForm,
                         UserUpdateForm)

from users.models import Profile


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = "profile"
    template_name = "users/profile/profile_detail.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Страница пользователя: {self.object.user.username}"
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "users/profile/profile_edit.html"
    form_class = ProfileUpdateForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "GameBlog - Profile"
        if self.request.POST:
            context["user_form"] = UserUpdateForm(
                self.request.POST, instance=self.request.user
            )
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context["user_form"]
        with transaction.atomic():
            if all([user_form.is_valid(), form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({"user_form": user_form})
                return self.render_to_response(context)
        return super(UserProfileUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print('in invalid')
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_detail", kwargs={"slug": self.request.user.profile.slug}
        )
