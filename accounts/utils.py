from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
import random


def login_required(r='accounts:login'):
    def deco(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return func(request, *args, **kwargs)
            return redirect(r)

        return wrapper

    return deco


def has_permissions(role):
    def deco(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.role == role:
                    return func(request, *args, **kwargs)
                raise PermissionDenied
            return redirect('accounts:login')
        return wrapper

    return deco


def code_generate():
    code = random.randint(1000, 9999)
    return code

from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != "Admin":
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

