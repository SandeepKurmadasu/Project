# import json
# import time
# from threading import Lock
# from django.http import JsonResponse
#
# RATE_LIMIT = 5         # max requests per second
# WINDOW_SIZE = 1        # seconds window for counting requests
# COOLDOWN_PERIOD = 60   # seconds to block after hitting limit
#
# # Store request timestamps per user/IP
# request_history = {}
# # Store cooldown expiry timestamp per user/IP
# cooldown_expiry = {}
#
# lock = Lock()  # to protect shared dict in multi-threaded env
#
# class RateLimitMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Apply only to /graphql endpoint
#         if not request.path.startswith("/graphql"):
#             return self.get_response(request)
#
#         try:
#             body = request.body.decode("utf-8")
#             data = json.loads(body)
#             query = data.get("query", "")
#         except Exception:
#             return self.get_response(request)
#
#         if "userLogin" not in query:
#             return self.get_response(request)
#
#         if request.user.is_authenticated:
#             identifier = f"user:{request.user.id}"
#         else:
#             identifier = f"ip:{self._get_ip(request)}"
#
#         now = time.time()
#
#         with lock:
#             # Check if user is in cooldown
#             cooldown_end = cooldown_expiry.get(identifier)
#             if cooldown_end and now < cooldown_end:
#                 # Still in cooldown period — block request
#                 retry_after = int(cooldown_end - now)
#                 response = JsonResponse(
#                     {
#                         "error": "Too Many Requests",
#                         "retry_after_seconds": retry_after
#                     },
#                     status=429,
#                 )
#                 response["Retry-After"] = str(retry_after)
#                 return response
#
#             # Not in cooldown, process timestamps
#             timestamps = request_history.get(identifier, [])
#             # Remove timestamps outside WINDOW_SIZE
#             timestamps = [t for t in timestamps if now - t < WINDOW_SIZE]
#
#             if len(timestamps) >= RATE_LIMIT:
#                 # Hit rate limit — start cooldown
#                 cooldown_expiry[identifier] = now + COOLDOWN_PERIOD
#                 # Clear timestamps to reset after cooldown
#                 request_history[identifier] = []
#                 response = JsonResponse(
#                     {
#                         "error": "Too Many Requests",
#                         "retry_after_seconds": COOLDOWN_PERIOD
#                     },
#                     status=429,
#                 )
#                 response["Retry-After"] = str(COOLDOWN_PERIOD)
#                 return response
#
#             # Record current request timestamp
#             timestamps.append(now)
#             request_history[identifier] = timestamps
#
#         return self.get_response(request)
#
#     def _get_ip(self, request):
#         x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(",")[0].strip()
#         else:
#             ip = request.META.get("REMOTE_ADDR")
#         return ip


import json
from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from course_management.models import RateLimitEntry

RATE_LIMIT = 5  # max requests per second
WINDOW_SIZE = 2  # seconds window for counting requests
COOLDOWN_PERIOD = 60  # seconds to block after hitting limit


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to GraphQL endpoints
        if not request.path.startswith("/graphql"):
            return self.get_response(request)

        # Parse request body to check for userLogin query
        try:
            body = request.body.decode("utf-8")
            data = json.loads(body)
            query = data.get("query", "")
        except Exception:
            return self.get_response(request)

        # Only rate limit userLogin queries
        if "userLogin" not in query:
            return self.get_response(request)

        # Get identifier (user ID or IP address)
        if hasattr(request, 'user') and request.user.is_authenticated:
            identifier = f"user:{request.user.id}"
        else:
            identifier = f"ip:{self._get_ip(request)}"

        now = timezone.now()

        # Get or create the rate limit entry (FIXED)
        entry, created = RateLimitEntry.objects.get_or_create(
            identifier=identifier,
            defaults={
                'last_requests': [],
                'cooldown_until': None
            }
        )

        # Check if user is in cooldown period
        if entry.cooldown_until and entry.cooldown_until > now:
            retry_after = int((entry.cooldown_until - now).total_seconds())
            return self.too_many_requests_response(retry_after)

        # Clean up old requests outside the window
        entry.last_requests = [
            ts for ts in entry.last_requests
            if now.timestamp() - ts < WINDOW_SIZE
        ]

        # Check if rate limit exceeded
        if len(entry.last_requests) >= RATE_LIMIT:
            entry.cooldown_until = now + timedelta(seconds=COOLDOWN_PERIOD)
            entry.last_requests = []
            entry.save()
            return self.too_many_requests_response(COOLDOWN_PERIOD)

        # Add current request timestamp and save
        entry.last_requests.append(int(now.timestamp()))
        entry.save()

        return self.get_response(request)

    @staticmethod
    def _get_ip(request):
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    @staticmethod
    def too_many_requests_response(retry_after_seconds):
        """Return 429 Too Many Requests response"""
        response = JsonResponse({
            "error": "Too Many Requests",
            "message": "You have exceeded the rate limit for login attempts.",
            "retry_after_seconds": retry_after_seconds,
        }, status=429)
        response["Retry-After"] = str(retry_after_seconds)
        return response