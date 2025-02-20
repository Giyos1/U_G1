from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.forms import UserRegisterForm, LoginForm, ProfileEditForm
from accounts.utils import login_required


# from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        forms = UserRegisterForm(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.set_password(forms.cleaned_data["password"])
            forms.save()
            login(request, user)
            return redirect("accounts:list")
        return render(request, "accounts/register.html", {"forms": forms})
    forms = UserRegisterForm()
    return render(request, "accounts/register.html", {"forms": forms})


@login_required()
def user_list(request):
    users = User.objects.all()
    return render(request, "accounts/user_list.html", {"users": users})


def login_user(request):
    if request.method == "POST":
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data["username"]
            password = forms.cleaned_data["password"]
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                login(request, user)
                return redirect("accounts:list")
            forms.add_error(None, "Username or password is incorrect")
        return render(request, "accounts/login.html", {"forms": forms})
    forms = LoginForm()
    return render(request, "accounts/login.html", {"forms": forms})


def logout_user(request):
    logout(request)
    return redirect("accounts:login")


@login_required()
def profile(request):
    user = request.user
    return render(request, "accounts/profile.html", {"user": user})


@login_required()
def profile_edit(request):
    if request.method == "POST":
        forms = ProfileEditForm(request.POST, instance=request.user)
        if forms.is_valid():
            forms.save()
            return redirect("accounts:profile")
        return render(request, "accounts/profile_edit.html", {"forms": forms, "user": request.user})
    forms = ProfileEditForm(instance=request.user)
    return render(request, "accounts/profile_edit.html", {"forms": forms})
