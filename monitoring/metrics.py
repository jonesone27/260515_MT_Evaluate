from prometheus_client import Counter
# see https://prometheus.github.io/client_python/instrumenting/counter/

translation_requests = Counter(
    "translation_requests_total",
    "Number of translation requests",
    ("provider",)
)