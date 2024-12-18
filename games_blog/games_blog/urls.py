"""
URL configuration for games_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from blog.feeds import LatestArticleFeed
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView
from services.utils import set_language

handler403 = "blog.views.exceptions_views.handler403"
handler404 = "blog.views.exceptions_views.handler404"
handler500 = "blog.views.exceptions_views.handler500"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("blog:articles")), name="home"),
    path("articles/", include("blog.urls", namespace="blog")),
    path("users/", include("users.urls", namespace="users")),
    path("chat/", include("chat.urls", namespace="chat")),
    path("api/", include("api.urls", namespace="api")),
    path("admin/", admin.site.urls),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("captcha/", include("captcha.urls")),
    path("ckeditor/", include("django_ckeditor_5.urls")),
    path("rosetta/", include("rosetta.urls")),
    path("feeds/latest/", LatestArticleFeed(), name="latest_post_feed"),
    path("set_language/", set_language, name="set_language"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
