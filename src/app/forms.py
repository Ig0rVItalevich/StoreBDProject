from django import forms
from django.core.exceptions import ValidationError
from app.models import Product, Review, Profile
from perfume.settings import MEDIA_URL


class LoginForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["username", "password"]

    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")


class RegisterForm(forms.Form):
    username = forms.CharField(label="Логин")
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}),
        label="Дата рождения",
    )
    sex = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Male/Female"}), label="Пол"
    )
    address = forms.CharField(label="Адрес")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(), label="Повторите пароль"
    )
    avatar = forms.FileField(label="Фото", required=False)

    def clean(self):
        cleaned_data = super().clean()

        passwd_one = cleaned_data["password"]
        passwd_two = cleaned_data["password_repeat"]

        sex = cleaned_data["sex"]

        if len(passwd_one) < 8:
            self.add_error(None, "Too short password (minimum 8 characters)!")

        if passwd_one != passwd_two:
            self.add_error(None, "Passwords do not match!")

        if sex != "Male" and sex != "Female":
            self.add_error(None, 'Field "sex" filled incorrectly!')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Введите сюда свой комментарий.",
                    "rows": "8",
                }
            )
        }


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["email", "first_name", "last_name", "address"]

    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    address = forms.CharField(label="Адрес")
    avatar = forms.FileField(widget=forms.FileInput(), label="Фото", required=False)


class SearchForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title"]

    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Поиск"}))
