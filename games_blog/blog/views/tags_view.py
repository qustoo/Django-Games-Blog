from blog.models import Article
from django.shortcuts import get_object_or_404
from django.views.generic import ListView


class ArticleListByTag(ListView):
    model = Article
    template_name = "blog/articles/articles.html"
    context_object_name = "articles"
    paginate_by = 2
    tag_instance = None

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag_slug")
        if tag_slug:
            self.tag_instance = get_object_or_404(Tag, slug=tag_slug)
            return Article.published.all().filter(tags__in=[self.tag_instance])
        else:
            return Article.published.all()
