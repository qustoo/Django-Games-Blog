from blog.forms import CommentCreateGuestForm, CommentCreateUserForm
from blog.mixins import GetCacheCategoriesMixin, ViewCountMixin
from blog.models import Article
from django.db.models import Count
from django.utils.translation import gettext
from django.views.generic import DetailView, ListView


class ArticleDetailView(ViewCountMixin, GetCacheCategoriesMixin, DetailView):
    model = Article
    context_object_name = "article"
    template_name = "blog/articles/articles_detail.html"

    def get_queryset(self):
        article_slug = self.kwargs.get("slug")
        return Article.published.detail(article_slug)

    def get_similar_articles(self):
        post_tags_ids = self.object.tags.values_list("id", flat=True)
        similar_posts = Article.published.filter(tags__in=post_tags_ids)
        similar_posts = similar_posts.exclude(slug=self.object.slug)
        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-publish"
        )
        return similar_posts

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context["title"] = self.object.title  # object - инстанс нашей статьи
        context["comments"] = self.object.comments.filter(active=True)

        context["similar_articles"] = self.get_similar_articles()
        context["form"] = (
            CommentCreateUserForm
            if self.request.user.is_authenticated
            else CommentCreateGuestForm
        )
        return context

class ArticleListView(GetCacheCategoriesMixin, ListView):
    context_object_name = "articles"
    template_name = "blog/articles/articles.html"
    paginate_by = 2

    def get_queryset(self):
        articles = Article.published.all()
        return articles

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context["title"] = gettext("Главная страница")
        return context
