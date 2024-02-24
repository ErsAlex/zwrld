from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import AccessMixin




def login_required_and_superuser(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return login_required(view_func)(request, *args, **kwargs)
        elif not request.user.is_superuser:
            return HttpResponseForbidden("Доступ запрещен") 
        return view_func(request, *args, **kwargs)
    return wrapped_view


class LoginAndAdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_superuser:
            return HttpResponseForbidden("Доступ запрещен") 
        return super().dispatch(request, *args, **kwargs)