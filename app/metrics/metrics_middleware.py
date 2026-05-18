import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .metrics_service import http_requests_total, http_request_duration_seconds


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path.startswith("/metrics"):
            return await call_next(request)

        method = request.method
        route = request.url.path

        timer = http_request_duration_seconds.labels(method=method, route=route).time()
        timer.__enter__()
        try:
            response = await call_next(request)
        finally:
            timer.__exit__(None, None, None)

        http_requests_total.labels(
            method=method,
            status=str(response.status_code),
            route=route,
        ).inc()

        return response
