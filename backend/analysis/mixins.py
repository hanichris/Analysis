from urllib.parse import urlparse

from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy


class AsyncLoginRequiredMixin(AccessMixin):
    login_url = reverse_lazy('login')

    async def dispatch(self, request: HttpRequest, *args, **kwargs):
        user = await request.auser() # type: ignore
        if not user.is_authenticated:
            return await self.handle_no_permission()
        return await super().dispatch(request, args, kwargs) # type: ignore
    
    async def handle_no_permission(self) -> HttpResponseRedirect:
        path = self.request.build_absolute_uri() # type: ignore
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path() # type: ignore
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )

class AsyncUserPassesTestMixin(AccessMixin):
    login_url = reverse_lazy('login')

    async def dispatch(self, request: HttpRequest, *args, **kwargs):
        user = await request.auser() # type: ignore
        if not await self.test_func(user):
            return await self.handle_no_permission()
        return await super().dispatch(request, args, kwargs) # type: ignore
    
    async def handle_no_permission(self) -> HttpResponseRedirect:
        path = self.request.build_absolute_uri() # type: ignore
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path() # type: ignore
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )
    
    async def test_func(self, user):
        """Checks if the current user has administrative priviledges.

        This method can be overriden in whichever class-based views that utilise the mixin.
        """
        return user.is_staff and user.is_superuser