from blog.models import Article
from django.core.cache import cache
from django.http import Http404
from django.views.generic import ListView


class ArticleSortListView(ListView):
    acceptable_filter_fields = ("id", "created_at", "author", "title")
    filter_fields_mapping = {"id": "pk"} | {k: k for k in acceptable_filter_fields}
    context_object_name = "articles"
    template_name = "blog/articles/sorted_articles.html"

    def get_queryset(self):
        filter_field = self.kwargs.get("filter")
        direction = self.kwargs.get("direction")

        if filter_field not in self.acceptable_filter_fields:
            raise Http404("Invalid direction filter field.")

        return self.get_ordered_queryset(filter_field, direction)

    def get_ordered_queryset(self, filter_field, direction):
        cached_articles = Article.published.all().order_by(
            "-" + self.filter_fields_mapping[filter_field]
            if direction == "DESC"
            else self.filter_fields_mapping[filter_field]
        )
        filtered_articles = cache.get_or_set(
            f"cached_filtered_articles_{filter_field}", cached_articles
        )
        return filtered_articles
