from django.shortcuts import redirect


def login_required(path="accounts:login"):
    def inner(func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(path)
            return func(request, *args, **kwargs)

        return wrapper

    return inner
