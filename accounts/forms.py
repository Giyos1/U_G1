from django import forms
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    re_password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 're_password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('Passwords do not match')
        return re_password

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])  # Parolni shifrlash
    #     if commit:
    #         user.save()
    #     return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


