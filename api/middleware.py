import time
from typing import Any, Callable
from django.core.cache import cache
from django.http import HttpRequest, JsonResponse


class HighFrequencyThrottleMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], Any]) -> None:
        self.get_response = get_response
        # Limit configurations: Max 60 requests per minute
        self.rate_limit = 60
        self.window_seconds = 60

    def __call__(self, request: HttpRequest) -> Any:
        # Only enforce throttling on our API landscape endpoints
        if request.path.startswith("/api/"):
            client_ip = self.get_client_ip(request)
            cache_key = f"throttle_{client_ip}"

            # Retrieve request timestamps history list from cache
            request_timestamps: list[float] = cache.get(cache_key, [])
            current_time = time.time()

            # Evict outdated timestamps from the sliding monitoring window
            request_timestamps = [
                t for t in request_timestamps if current_time - t < self.window_seconds
            ]

            if len(request_timestamps) >= self.rate_limit:
                return JsonResponse(
                    {"error": "API rate limit exceeded. Retry in a minute."},
                    status=429,
                )

            # Log current request and commit updated history list to cache
            request_timestamps.append(current_time)
            cache.set(cache_key, request_timestamps, self.window_seconds)

        return self.get_response(request)

    def get_client_ip(self, request: HttpRequest) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return str(x_forwarded_for.split(",")[0].strip())
        return str(request.META.get("REMOTE_ADDR", "unknown"))
