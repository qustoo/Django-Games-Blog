from api.views import ArticleDetail, ArticleList, UserArticleList
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

app_name = "api"
urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger-ui",
    ),
    path("", ArticleList.as_view(), name="article_list"),
    path("user/<str:username>/", UserArticleList.as_view(), name="user_article_list"),
    path("<slug:slug>/", ArticleDetail.as_view(), name="article_detail"),
]
