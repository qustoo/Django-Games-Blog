from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from blog.forms import CategoryCreateForm, CategoryUpdateForm
from blog.mixins import AuthorRequiredMixin
from blog.models import Article, Category
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from games_blog.settings import PAGINATE_BY


class CategoriesListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'blog/categories/list_categories.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление категории"
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "blog/categories/category_create.html"
    form_class = CategoryCreateForm
    login_url = "/users/login/"
    success_url = reverse_lazy("blog:categories")



class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    template_name = "blog/categories/category_update.html"
    context_object_name = "article"
    form_class = CategoryUpdateForm
    success_url = reverse_lazy("blog:categories")
    success_message = "Материал успешно обновлен"


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy("blog:categories")
    context_object_name = "category"
    template_name = "blog/categories/category_delete.html"



class ArticleByCategoryListView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "blog/articles/articles.html"
    paginate_by = PAGINATE_BY

    selected_category = None

    def get_queryset(self):
        category_slug = self.kwargs.get("slug")
        self.selected_category = get_object_or_404(Category, slug=category_slug)
        queryset = Article.published.filter(category__slug=self.selected_category.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.kwargs.get("page", 1)
        page_nums = context["paginator"].num_pages
        if int(page) > page_nums:
            context["page_obj"] = context["paginator"].get_page(page_nums)

        context["title"] = f"Статьи из категории: {self.selected_category.title}"
        return context
