from blog.models import Article, ArticleView, Category, Comment, Rating
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "status", "tags")
    list_display_links = ("title", "slug")
    list_filter = ("status", "category")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ("tree_actions", "indented_title", "id", "title", "slug")
    list_display_links = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin):
    list_display = (
        "tree_actions",
        "indented_title",
        "article",
        "author",
        "created_at",
        "status",
    )
    mptt_level_indent = 2
    list_display_links = ("article", "created_at")
    list_filter = ("created_at", "updated_at", "author")
    list_editable = ("status",)


@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    pass
