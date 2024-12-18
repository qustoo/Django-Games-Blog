from blog.forms import ArticleCreateForm, ArticleUpdateForm
from blog.mixins import AuthorRequiredMixin
from blog.models import Article
from blog.tasks import publish_article_scheduled
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from services.utils import delete_cache_keys


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "blog/articles/articles_create.html"
    form_class = ArticleCreateForm
    success_url = reverse_lazy("blog:articles")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление статьи на сайт"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        publish_time = form.cleaned_data["publish"]
        form.save()
        delete_cache_keys()
        publish_article_scheduled.apply_async(args=[form.instance.id], eta=publish_time)
        return super().form_valid(form)


class ArticleUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Article
    template_name = "blog/articles/articles_update.html"
    context_object_name = "article"
    form_class = ArticleUpdateForm
    success_url = reverse_lazy("blog:articles")
    success_message = "Материал успешно обновлен"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Обновление статьи: {self.object.title}"
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        delete_cache_keys()
        return super().form_valid(form)

    def form_invalid(self, form):
        print('ArticleUpdateView invalid')
        print(form.errors)
        return super().form_invalid(form)


class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("blog:articles")
    context_object_name = "article"
    template_name = "blog/articles/articles_delete.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Удаление статьи: {self.object.title}"
        return context

    def form_valid(self, form):
        delete_cache_keys()
        return super().form_valid(form)
