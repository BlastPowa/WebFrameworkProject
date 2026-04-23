# decorator for checking user role before allowing acces to a view
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def role_required(*allowed_roles):

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
