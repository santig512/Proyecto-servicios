from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST, Counter
from fastapi import Response

REQUESTS = Counter('ps_requests_total', 'Total HTTP requests')


def metrics_endpoint():
    registry = CollectorRegistry()
    # Register custom metrics to the default registry instead for simplicity
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
