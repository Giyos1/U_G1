from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_changed
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from django.utils import timezone

from accounts.models import Code


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
        if self.instance:
            return self.instance.update(**self.cleaned_data)
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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise ValidationError('email topilmadi')
        return email


class RestorePasswordForm(forms.Form):
    username = forms.CharField(max_length=200)
    code = forms.CharField(max_length=4)
    password = forms.CharField(widget=PasswordInput)
    re_password = forms.CharField(widget=PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        code = self.cleaned_data.get('code')
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError("username topilmadi")

        if not Code.objects.filter(user=user, code_number=code, expired_data__gt=timezone.now()):
            raise ValidationError(f"code topilmadi {timezone.now()}")

        if password != re_password:
            raise ValidationError("passwor most emas topilmadi")

        return self.cleaned_data

    def update(self):
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        user.set_password(self.cleaned_data.get('password'))
        user.save()
