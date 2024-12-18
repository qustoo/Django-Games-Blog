from blog.forms import EmailShareArticleForm
from blog.models import Article
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView


class ArticleShareView(FormView):
    template_name = "blog/widgets/share_post.html"
    form_class = EmailShareArticleForm
    success_url = reverse_lazy("blog:share")
    send_status = None

    def get_article_by_slug(self, slug):
        return get_object_or_404(Article, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_slug = self.kwargs.get("slug")
        article = self.get_article_by_slug(article_slug)
        context["title"] = "Отправка поста по email"
        context["article"] = article
        context["send_status"] = bool(self.send_status)
        context["form"] = self.form_class(data=self.request.POST)
        return context

    def form_valid(self, form):
        article_slug = self.kwargs.get("article_slug")
        article = self.get_article_by_slug(article_slug)
        article_url = self.request.build_absolute_uri(article.get_absolute_url())
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        to = form.cleaned_data["to"]
        comments = form.cleaned_data["comments"]
        send_mail(
            subject=f"{name} recommends you read: {article_url}",
            message=f"Read {article.title} as {article_url} \n\n"
            f"Send from {name} \n\n"
            f"Commends: {comments} \n\n",
            from_email=email,
            recipient_list=[
                to,
            ],
        )
        self.get_context_data(send_status=True, form=form)
        self.send_status = True
        return self.render_to_response(self.get_context_data())
