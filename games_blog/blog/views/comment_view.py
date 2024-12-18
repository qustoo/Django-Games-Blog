from http import HTTPStatus

from blog.forms import CommentCreateGuestForm, CommentCreateUserForm
from blog.models import Article, Comment
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View


class CommentCreatePostView(View):

    def is_ajax(self):
        return self.request.headers.get("X-Requested-With") == "XMLHttpRequest"

    def dispatch(self, request, *args, **kwargs):
        if request.method != "POST":
            return HttpResponseNotAllowed(request.method)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article.published, slug=self.kwargs.get("slug"))
        guest_status = not request.user.is_authenticated

        form = (
            CommentCreateUserForm(request.POST)
            if request.user.is_authenticated
            else CommentCreateGuestForm(request.POST)
        )
        comment = None
        if form.is_valid():
            cleaned_data = form.cleaned_data
            comment = Comment(
                content=cleaned_data["content"],
                article_id=article.id,
            )
            if guest_status:
                username = cleaned_data["name"]
                email = cleaned_data["email"]
                comment.name = username
                comment.email = email
                comment.parent_id = cleaned_data["parent"]
            else:
                comment.author = request.user
                comment.name = request.user.username
                comment.email = request.user.email
                comment.parent_id = cleaned_data["parent"]

            comment.save()

        if self.is_ajax():
            data = {
                "is_child": comment.is_child_node(),
                "id": comment.id,
                "author": comment.author.username if not guest_status else "",
                "parent_id": comment.parent_id,
                "time_create": comment.created_at.strftime("%Y-%b-%d %H:%M:%S"),
                "avatar": (
                    comment.author.profile.avatar.url
                    if not guest_status
                    else "avatars/default.jpg"
                ),
                "content": comment.content,
                "get_absolute_url": (
                    comment.author.profile.get_absolute_url()
                    if not guest_status
                    else ""
                ),
            }
            return JsonResponse(data=data, status=HTTPStatus.OK)
        return redirect(article.get_absolute_url())
