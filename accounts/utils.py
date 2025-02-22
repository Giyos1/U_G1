from django.shortcuts import redirect


def login_required(r='accounts:login'):
    def deco(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return func(request, *args, **kwargs)
            return redirect(r)

        return wrapper

    return deco
