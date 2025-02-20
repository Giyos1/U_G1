from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    re_password = forms.CharField(max_length=200, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 're_password']
        widgets = {
            "password": forms.PasswordInput()
        }

    # def clean_username(self):
    #     if User.objects.filter(self.cleaned_data.get('username')).exists():
    #         raise ValidationError("username already exist")
    #     return self.cleaned_data.get('username')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        re_password = cleaned_data['re_password']

        if password != re_password:
            raise ValidationError("password not equeal re_password")
        cleaned_data.pop('re_password')
        return cleaned_data

    def save(self, commit=True):
        return User.objects.create_user(**self.cleaned_data)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("password yoki username xato")
        return cleaned_data


