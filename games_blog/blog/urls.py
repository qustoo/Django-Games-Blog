from blog.views import *
from django.urls import path

from blog.views.categories_view import CategoriesListView, CategoryCreateView

app_name = "blog"
urlpatterns = [
    # All Articles
    path("", ArticleListView.as_view(), name="articles"),

    # Detail View
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="article_detail",
    ),
    # CRUD Categories
    path("categories/", CategoriesListView.as_view(), name="categories"),
    path("categories/create/", CategoryCreateView.as_view(), name="categories_create"),
    path("categories/<slug:slug>/update", CategoryCreateView.as_view(), name="categories_create"),

    # CRUD Articles
    path("create/", ArticleCreateView.as_view(), name="articles_create"),
    path("<str:slug>/update", ArticleUpdateView.as_view(), name="articles_update"),
    path("<str:slug>/delete/", ArticleDeleteView.as_view(), name="articles_delete"),

    # Articles by category
    path(
        "category/<slug:slug>",
        ArticleByCategoryListView.as_view(),
        name="articles_by_category",
    ),
    # Pagination
    path("page/<int:page>/", ArticleListView.as_view(), name="paginator"),
    # Share by email
    path("share/<slug:slug>", ArticleShareView.as_view(), name="share"),
    path("search/", ArticleSearchFormView.as_view(), name="search"),
    path("tag/<slug:tag_slug>/", ArticleListByTag.as_view(), name="post_list_by_tag"),
    path(
        "<slug:slug>/comments/create/",
        CommentCreatePostView.as_view(),
        name="article_comment",
    ),
    path("rating/", RatingCreateView.as_view(), name="rating"),
    path(
        "sort/<str:filter>/<str:direction>/",
        ArticleSortListView.as_view(),
        name="article_list_sort",
    ),
]
