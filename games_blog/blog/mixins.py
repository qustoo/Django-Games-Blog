from blog.models import ArticleView, Category
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.core.cache import cache
from django.shortcuts import redirect
from services.utils import get_client_ip


class GetCacheCategoriesMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_categories = cache.get("cached_categories")
        if cache_categories:
            context["categories"] = cache_categories
        return context


class AuthorRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if request.user != self.get_object().author:
                messages.info(
                    request, "Изменение и удаление статьи доступно только автору"
                )
                return redirect("home")
        return super().dispatch(request, *args, **kwargs)


class ViewCountMixin:
    def get_object(self):
        obj = super().get_object()
        ip_address = get_client_ip(self.request)
        ArticleView.objects.get_or_create(article=obj, ip_address=ip_address)
        return obj
