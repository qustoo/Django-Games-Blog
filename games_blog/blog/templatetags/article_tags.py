from datetime import timedelta

import markdown
from django.utils import timezone

from blog.models import Article, Category
from django import template
from django.db.models import Count, Q
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def count_articles():
    return Article.published.count()


@register.simple_tag()
def popular_articles_by_period(days = 7):
    now = timezone.now()
    certain_viewed_on_date = now - timedelta(days=days)
    articles = Article.published.annotate(total_view = Count("views", filter=Q(views__viewed_on__gte=certain_viewed_on_date))).prefetch_related('views')
    popular_articles = articles.order_by('-total_view')[:10]
    return popular_articles


@register.inclusion_tag("blog/categories/categories.html")
def all_categories():
    categories = Category.objects.all()
    return {"categories": categories}


@register.inclusion_tag("blog/widgets/last_articles.html")
def show_latest_articles(count=2):
    latest_articles = Article.published.all().order_by("-publish")[:count]
    return {"latest_articles": latest_articles}


@register.inclusion_tag("blog/widgets/most_commented_articles.html")
def get_most_commented_articles(count=5):
    commented_articles = (
        Article.published.annotate(
            total_comments=Count("comments", filter=Q(comments__active=True))
        )
        .exclude(total_comments=0)
        .order_by("-total_comments")[:count]
    )
    return {"commented_articles": commented_articles}


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
