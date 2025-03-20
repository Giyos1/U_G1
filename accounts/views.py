from django.contrib.auth import login, authenticate, logout
from django.contrib.sessions.models import Session
from django.db.models import F, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import User, UserRole
from accounts.forms import UserForm, LoginForm, ProfileForm, ForgotPasswordForm, RestorePasswordForm, \
    TransactionCreateForm
from django.contrib.auth.decorators import login_required, permission_required

from accounts.service import send_email_alternative, send_email_async, otp_code_send_async
from config import settings
import requests


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


@permission_required('contact.view_contact', raise_exception=True)
def dashboard(request):
    user = User.objects.all().annotate(contact_count=Count('user_contact'))
    return render(request, 'admin/dashboard.html', {"user": user})


def create_transaction(request):
    if request.method == 'POST':
        form = TransactionCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts:contact_list')
        return render(request, 'transaction/create_transaction.html', {'form': form})
    forms = TransactionCreateForm()
    return render(request, 'transaction/create_transaction.html', {'form': forms})


def session_data_get_decode(request):
    session_id = request.COOKIES.get('sessionid')
    session = Session.objects.get(session_key=session_id)
    # print(request.META)

    session_data = session.get_decoded()
    # for key, value in session_data.items():
    #     print(key, value)
    return HttpResponse('session data')


def google_login(request):
    auth_url = (
        f"{settings.GOOGLE_AUTH_URL}"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return redirect(auth_url)


def google_callback(request):
    code = request.GET.get("code")

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(settings.GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    user_info_response = requests.get(settings.GOOGLE_USER_INFO_URL,
                                      headers={"Authorization": f"Bearer {access_token}"})

    user_info = user_info_response.json()
    user, _ = User.objects.get_or_create(google_id=user_info.get("id"),
                                         username=user_info.get("email"),
                                         email=user_info.get("email"),
                                         image=user_info.get("picture"),
                                         first_name=user_info.get("given_name"),
                                         last_name=user_info.get("family_name"),
                                         )
    login(request, user)

    if user.is_2fa_enabled:
        return redirect('accounts:2fa')
    return redirect('accounts:profile')


def two_factor_auth(request):
    if request.method == 'POST':
        otp = request.POST.get('2fa_code')
        user = request.user
        if user.verify_otp(otp):
            return redirect('accounts:profile')
        return render(request, 'accounts/2fa.html', {'error': 'OTP xato'})
    otp_code_send_async(request.user)
    return render(request, 'accounts/2fa.html')
