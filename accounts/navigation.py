from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


def previous_page(request):
    referer = request.META.get("HTTP_REFERER")

    if referer and url_has_allowed_host_and_scheme(
        referer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return {
            "previous_page_url": referer,
        }

    return {
        "previous_page_url": reverse("home"),
    }
