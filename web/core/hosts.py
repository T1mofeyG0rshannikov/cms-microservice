from django.conf import settings
from django_hosts import host, patterns

host_patterns = patterns(
    "",
    host(r"www", settings.ROOT_URLCONF, name="www"),
    # host(r'api', settings.ROOT_URLCONF, name='api'),
)
