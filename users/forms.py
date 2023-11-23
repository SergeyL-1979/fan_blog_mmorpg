from allauth.account.forms import LoginForm, SignupForm, BaseSignupForm
from django import forms
from django.forms import (
    ModelForm, CharField, TextInput, EmailInput, PasswordInput, EmailField)
from django.core.exceptions import ValidationError
from users.models import CustomUser


class UserForm(ModelForm):
    """Модельная форма редактировать профиль"""

    class Meta:
        model = CustomUser

        fields = ['username', 'first_name', 'last_name', 'email', ]

        labels = {'username': 'Логин', 'first_name': 'Имя',
                  'last_name': 'Фамилия', 'email': 'email', }

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'width:40ch ',
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...',
                'style': 'width:40ch',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...',
                'style': 'width:40ch',
            }),
            'email': EmailInput(attrs={
                'multiple class': 'form-control',
                'style': 'width:40ch',
            }),
        }

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        # Достать всех пользователей с таким email, кроме себя
        if CustomUser.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован')
        return email


class MyLoginForm(LoginForm):
    # условие для применения ACCOUNT_FORMS в settings
    """Переопределить форму вхожа allauth"""

    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)

        self.fields['login'] = CharField(
            label=("E-MAIL"), widget=TextInput(attrs={'class': 'form-control', }))
        self.fields['password'].widget = PasswordInput(
            attrs={'class': 'form-control', })


class MySignupForm(SignupForm):
    # можно по разному переопределять форму. Так:
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           "type": "email",
                                                           "placeholder": "E-mail address",
                                                           "autocomplete": "email",
                                                           }))
    # Добавьте свои поля, если необходимо
    activation_code = forms.CharField(max_length=30, required=False)

    def save(self, request):
        user = super(MySignupForm, self).save(request)
        # Дополнительная обработка, если необходимо
        user.activation_code = self.cleaned_data['activation_code']
        user.save()
        return user

    # или так:
    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget = PasswordInput(
            attrs={'class': 'form-control', })
        self.fields['password2'].widget = PasswordInput(
            attrs={'class': 'form-control', })

# class CustomSignupForm(SignupForm):
#     # Добавьте свои поля, если необходимо
#     activation_code = forms.CharField(max_length=30, required=False)
#
#     def save(self, request):
#         user = super(CustomSignupForm, self).save(request)
#         # Дополнительная обработка, если необходимо
#         user.activation_code = self.cleaned_data['activation_code']
#         user.save()
#         return user
