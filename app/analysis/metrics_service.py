from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR

registry = CollectorRegistry()

registry.register(PROCESS_COLLECTOR)
registry.register(PLATFORM_COLLECTOR)
registry.register(GC_COLLECTOR)

http_requests_total = Counter(
    name="http_requests_total",
    documentation="Total number of HTTP requests",
    labelnames=["method", "status", "route"],
    registry=registry,
)

http_request_duration_seconds = Histogram(
    name="http_request_duration_seconds",
    documentation="Duration of HTTP requests in seconds",
    labelnames=["method", "route"],
    buckets=[0.1, 0.5, 1, 2, 5, 10],
    registry=registry,
)


def get_metrics() -> tuple[bytes, str]:
    return generate_latest(registry), CONTENT_TYPE_LATEST
