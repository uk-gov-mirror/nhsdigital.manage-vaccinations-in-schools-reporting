from markupsafe import Markup

from mavis.reporting.helpers.reporting_context_helper import get_reporting_context

FALLBACK_ITEMS = [
    {"path": "/schools", "title": "Schools"},
    {"path": "/patients", "title": "Children"},
    {"path": "/sessions", "title": "Sessions"},
    {"path": "/vaccines", "title": "Vaccines"},
    {"path": "/consent-forms", "title": "Unmatched responses"},
    {"path": "/school-moves", "title": "School moves"},
    {"path": "/reports", "title": "Reports"},
    {"path": "/imports", "title": "Imports"},
    {"path": "/team", "title": "Your team"},
]


def build_navigation_items(request):
    items = get_reporting_context(request).get("navigation_items")
    if not isinstance(items, list):
        items = FALLBACK_ITEMS

    nav_items: list[dict] = []
    for item in items:
        nav_item: dict = {"href": item["path"], "text": item["title"]}

        if item["path"] == "/reports":
            nav_item["current"] = True

        if (count := item.get("count")) is not None:
            badge = (
                '<span class="app-count">'
                '<span class="nhsuk-u-visually-hidden"> (</span>'
                f"{count}"
                '<span class="nhsuk-u-visually-hidden">)</span>'
                "</span>"
            )
            nav_item["html"] = Markup(f"{item['title']}{badge}")
            nav_item["classes"] = "app-header__navigation-item--with-count"
            del nav_item["text"]

        nav_items.append(nav_item)

    return nav_items
