from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                return JsonResponse(
                    {"detail": "Authentication required."},
                    status=401
                )

            if user.role not in allowed_roles:
                return JsonResponse(
                    {"detail": "You do not have permission to perform this action."},
                    status=403
                )

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
