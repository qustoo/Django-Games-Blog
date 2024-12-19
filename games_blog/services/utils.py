from uuid import uuid4

from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import translation
from pytils.translit import slugify


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{unique_slug}-{uuid4().hex[:8]}"
    return unique_slug


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip_address = (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )
    return ip_address


def set_language(request):
    selected_user_language = request.GET.get("language", default="ru")
    translation.activate(selected_user_language)

    response = HttpResponseRedirect(reverse_lazy("home"))
    response.set_cookie("django_language", selected_user_language)

    return response


def delete_cache_keys():
    cache.delete(f"cached_categories")
    key_list = [
        f"cached_filtered_articles_{col}"
        for col in ("pk", "created_at", "author", "title")
    ]
    cache.delete_many(key_list)
