from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm, PasswordChangeForm)
from django.contrib.auth.models import User
from users.models import Profile


class UserLoginForm(AuthenticationForm):
    captcha = CaptchaField(
        label="Введите текст с картинки",
        error_messages={"invalid": "Не пройдена проверка капчи"},
        generator="captcha.helpers.math_challenge",
    )

    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы регистрации
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields["username"].widget.attrs["placeholder"] = "Логин пользователя"
            self.fields["password"].widget.attrs["placeholder"] = "Пароль пользователя"
            self.fields["username"].label = "Логин"
            self.fields["password"].label = "Пароль"
            if field != "remember_me":
                self.fields[field].widget.attrs.update(
                    {"class": "form-control mt-3 mb-3", "autocomplete": "off"}
                )


class UserRegistrationForm(UserCreationForm):
    captcha = CaptchaField(
        label="Введите текст с картинки",
        error_messages={"invalid": "Не пройдена проверка капчи"},
        generator="captcha.helpers.math_challenge",
    )

    first_name = forms.CharField(
        min_length=1,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-1 py-4", "placeholder": "Ваше имя"}
        ),
    )
    last_name = forms.CharField(
        min_length=1,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-1 py-4", "placeholder": "Ваше фамилия"}
        ),
    )
    username = forms.CharField(
        min_length=1,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-1 py-4", "placeholder": "Ваш логин"}
        ),
    )
    email = forms.CharField(
        min_length=1,
        widget=forms.EmailInput(
            attrs={"class": "form-control mb-1 py-4", "placeholder": "Ваша почта"}
        ),
    )
    password1 = forms.CharField(
        min_length=1,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-1 py-4",
                "placeholder": "Придумайте свой пароль",
            }
        ),
    )
    password2 = forms.CharField(
        min_length=1,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "Повторите придуманный пароль",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        if (
                email
                and User.objects.filter(email=email).exclude(username=username).exists()
        ):
            raise forms.ValidationError("This email is already registered.")
        return email.lower()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )

    def clean_email(self):
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        if (
                email
                and User.objects.filter(email=email).exclude(username=username).exists()
        ):
            raise forms.ValidationError("This email is already registered.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("birth_date", "bio", "avatar")

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "bio":
                self.fields[field].widget.attrs.update({"class": "django_ckeditor_5"})
            else:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control", "autocomplete": "off"}
                )


class UserPasswordChangeForm(PasswordChangeForm):
    """
    Форма изменения пароля
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )


class UserPasswordResetForm(PasswordResetForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )


class UserSetNewPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )
