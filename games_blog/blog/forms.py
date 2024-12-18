from captcha.fields import CaptchaField
from django_ckeditor_5.widgets import CKEditor5Widget

from blog.models import Article, Category, Feedback
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EmailShareArticleForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), max_length=35
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    to = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    comments = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}), required=False
    )


class ArticleCreateForm(forms.ModelForm):
    """
    Форма добавления статей на сайте
    """

    publish = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "placeholder": "Выберите дату и время",
                "type": "datetime-local",
            }
        ),
        initial=timezone.now,
    )

    class Meta:
        model = Article
        fields = (
            "title",
            "category",
            "full_description",
            "image",
        )

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "full_description":
                self.fields[field].widget.attrs.update({"class": "django_ckeditor_5"})
            else:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control", "autocomplete": "off"}
                )


class ArticleUpdateForm(ArticleCreateForm):
    """
    Форма обновления статьи на сайте
    """

    class Meta:
        model = Article
        fields = ArticleCreateForm.Meta.fields + ("status", "tags")

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )


class FeedbackCreateForm(forms.ModelForm):
    captcha = CaptchaField(
        label="Введите текст с картинки",
        error_messages={"invalid": "Не пройдена проверка капчи"},
        generator="captcha.helpers.math_challenge",
    )

    class Meta:
        model = Feedback
        fields = ("subject", "content")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "content":
                self.fields[field].widget.attrs.update({"class": "form-control django_ckeditor_5"})
            else:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control py-3", "autocomplete": "off"}
                )


class CommentBaseForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "cols": 30,
                "rows": 5,
                "placeholder": _("Комментарий"),
            }
        )
    )


class CommentCreateUserForm(CommentBaseForm):
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)


class CommentCreateGuestForm(CommentBaseForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Имя")}
        ),
        max_length=35,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Почта")}
        )
    )
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("title", "description", "parent")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class CategoryUpdateForm(CategoryCreateForm):
    pass
