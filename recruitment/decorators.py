"""
Custom access-control decorator for role-based views.

role_required ensures that the requesting user is authenticated and that the
UserProfile.role matches one of the allowed roles. When the check fails a
friendly "Access Denied" page is rendered with HTTP 403.
"""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def role_required(*allowed_roles):
    """Decorator factory that restricts a view to a set of profile roles."""

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            profile = getattr(request.user, 'profile', None)
            if profile is None or profile.role not in allowed_roles:
                context = {'allowed_roles': allowed_roles}
                return render(
                    request,
                    'recruitment/access_denied.html',
                    context,
                    status=403,
                )
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
