from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class RequestCounterMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counter_key = 'request_counter'

        self.request_counter = cache.get(self.request_counter_key)
        if self.request_counter is None:
            self.request_counter = 0
            cache.set(self.request_counter_key, self.request_counter)

    def __call__(self, request):
        self.request_counter += 1
        cache.set(self.request_counter_key, self.request_counter)

        response = self.get_response(request)
        return response
