from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Category


@receiver(post_save, sender=Category)
def update_categories_cache(sender, instance, **kwargs):
    cache.delete("cached_categories")
    categories = Category.objects.all()
    cache.set("cached_categories", categories)
