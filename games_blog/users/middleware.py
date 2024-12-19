from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

FIVE_MINUTES = 60 * 5


class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f"list-seen-{request.session.session_key}"
            last_login = cache.get(cache_key)
            if not last_login:
                last_login = timezone.now()
                User.objects.filter(id=request.user.id).update(last_login=last_login)

                cache.set(cache_key, last_login, FIVE_MINUTES)
