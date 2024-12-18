from blog.models import Article
from django.contrib.postgres.search import TrigramSimilarity
from django.views.generic import ListView


class ArticleSearchFormView(ListView):
    template_name = "blog/articles/articles.html"
    context_object_name = "articles"
    def get_queryset(self):
        if query := self.request.GET.get("query"):
            return (
                Article.published.annotate(similarity=TrigramSimilarity("title", query))
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )
        return Article.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("query")
        context["articles"] = self.get_queryset()
        return context
