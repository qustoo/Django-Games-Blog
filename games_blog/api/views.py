
from api.permissions import IsAuthorOrReadOnly
from api.serializers import ArticleSerializer
from blog.models import Article
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response


class ArticleList(ListAPIView):
    queryset = Article.published.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ["author"]
    search_fields = ["body", "author__username"]
    ordering_fields = ["author_id", "publish"]


class ArticleDetail(RetrieveUpdateDestroyAPIView):
    queryset = Article.published.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    permission_classes = (IsAuthorOrReadOnly,)


class UserArticleList(ListAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = ArticleSerializer
    # For generate schema
    queryset = Article.objects.none()

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs["username"])
        return Article.published.all().filter(author=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)

