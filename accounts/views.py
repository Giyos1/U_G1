from django.contrib.auth import login, authenticate, logout
from django.db.models import F, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import User, UserRole
from accounts.forms import UserForm, LoginForm, ProfileForm, ForgotPasswordForm, RestorePasswordForm
from django.contrib.auth.decorators import login_required

from accounts.service import send_email_alternative, send_email_async
from accounts.utils import has_permissions


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # user.set_password(form.cleaned_data.get('password'))
            # user.save()
            return redirect('contacts:contact_list')
        return render(request, 'accounts/register.html', {'form': form})
    form = UserForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data['username']).first()
            login(request, user)
            return redirect('contacts:contact_list')
        return render(request, "accounts/login.html", {"form": form})

        # v2
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        #
        # user = authenticate(username=username, password=password)
        # if user:
        #     login(request, user)
        #     return redirect('contacts:contact_list')
        # form.add_error(None, "password yoki username xato")
        # return render(request, "accounts/login.html", {"form": form})
        # v1
        # user = User.objects.filter(username=username).first()
        # if user:
        #     if user.check_password(password):
        #         login(request, user)
        #         return redirect('contacts:contact_list')
        # form.add_error(None,"password yoki username xato")
        # return render(request, "accounts/login.html", {"form": form})
    form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {"user": user})


@login_required
def profile_edit(request):
    if request.POST:
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        return render(request, 'accounts/profile_edit.html', {'form': form})
    form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            send_email_async(email, user)
            return HttpResponse("qabul qilindi borib emailinga qara!")
        return render(request, 'accounts/forgot_password.html', context={'form': form})
    form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', context={'form': form})


def restore_password(request):
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            form.update()
            return redirect('accounts:login')
        return render(request, 'accounts/restore.html', context={'form': form})
    form = RestorePasswordForm()
    return render(request, 'accounts/restore.html', context={'form': form})


@has_permissions(role=UserRole.ADMIN)
def dashboard(request):
    user = User.objects.all().annotate(contact_count=Count('user_contact'))
    return render(request, 'admin/dashboard.html', {"user": user})
