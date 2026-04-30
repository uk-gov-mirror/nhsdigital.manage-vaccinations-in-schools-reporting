from flask import current_app, url_for

from mavis.reporting.helpers import mavis_helper
from mavis.reporting.helpers.reporting_context_helper import get_reporting_context


def generate_secondary_nav_items(team_workgroup: str, current_page: str, request=None):
    items = [
        {
            "text": "Vaccinations",
            "href": url_for("main.vaccinations", workgroup=team_workgroup),
            "current": current_page == "vaccinations",
        },
        {
            "text": "Consent",
            "href": url_for("main.consent", workgroup=team_workgroup),
            "current": current_page == "consent",
        },
        {
            "text": "Schools",
            "href": url_for("main.schools", workgroup=team_workgroup),
            "current": current_page == "schools",
        },
        {
            "text": "Local authorities",
            "href": url_for("main.local_authorities", workgroup=team_workgroup),
            "current": current_page == "local_authorities",
        },
        {
            "text": "Download data",
            "href": url_for("main.start_download", workgroup=team_workgroup),
            "current": current_page == "download",
        },
    ]

    if get_reporting_context(request).get("careplus_reports_tab_visible") is True:
        items.append(
            {
                "text": "CarePlus reports",
                "href": mavis_helper.mavis_public_url(
                    current_app, "/careplus-reports/"
                ),
                "current": False,
            }
        )

    return items
