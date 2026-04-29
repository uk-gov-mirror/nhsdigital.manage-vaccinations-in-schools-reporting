import json
from urllib.parse import unquote_plus

from flask import current_app


def get_reporting_context(request):
    if request is None:
        return {}

    cookie_value = request.cookies.get("mavis_reporting_context")
    if not cookie_value:
        return {}

    try:
        parsed = json.loads(unquote_plus(cookie_value))
    except (json.JSONDecodeError, ValueError):
        current_app.logger.warning(
            "Failed to parse reporting context cookie: %s", cookie_value
        )
        return {}

    if not isinstance(parsed, dict):
        current_app.logger.warning(
            "Failed to parse reporting context cookie: %s", cookie_value
        )
        return {}

    return parsed
