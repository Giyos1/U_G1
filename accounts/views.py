from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from accounts.forms import UserForm, LoginForm


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
