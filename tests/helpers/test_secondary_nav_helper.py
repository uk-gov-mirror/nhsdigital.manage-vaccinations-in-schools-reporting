import json
from urllib.parse import quote_plus

import pytest
from flask import Flask

from mavis.reporting.helpers import secondary_nav_helper
from tests.conftest import MockRequest


@pytest.fixture()
def app():
    return Flask(__name__)


@pytest.fixture(autouse=True)
def stub_navigation_urls(monkeypatch):
    monkeypatch.setattr(
        secondary_nav_helper,
        "url_for",
        lambda endpoint, workgroup: f"/{endpoint.split('.')[-1]}/{workgroup}",
    )
    monkeypatch.setattr(
        secondary_nav_helper.mavis_helper,
        "mavis_public_url",
        lambda _app, path: f"https://example.com{path}",
    )


def reporting_context_cookie(*, careplus_reports_tab_visible=None):
    payload = {}
    if careplus_reports_tab_visible is not None:
        payload["careplus_reports_tab_visible"] = careplus_reports_tab_visible

    return quote_plus(json.dumps(payload))


@pytest.mark.parametrize(
    ("cookie_value", "expected_count"),
    [(None, 5), (False, 5), (True, 6)],
)
def test_careplus_cookie_controls_tab_visibility(cookie_value, expected_count):
    cookies = {}
    if cookie_value is not None:
        cookies["mavis_reporting_context"] = reporting_context_cookie(
            careplus_reports_tab_visible=cookie_value
        )

    items = secondary_nav_helper.generate_secondary_nav_items(
        "r1l",
        "vaccinations",
        request=MockRequest(cookies=cookies),
    )

    assert len(items) == expected_count


def test_careplus_tab_is_appended_when_cookie_is_true():
    items = secondary_nav_helper.generate_secondary_nav_items(
        "r1l",
        "vaccinations",
        request=MockRequest(
            cookies={
                "mavis_reporting_context": reporting_context_cookie(
                    careplus_reports_tab_visible=True
                )
            }
        ),
    )

    assert items[-1] == {
        "text": "CarePlus reports",
        "href": "https://example.com/careplus-reports/",
        "current": False,
    }


def test_current_page_is_marked_current():
    items = secondary_nav_helper.generate_secondary_nav_items(
        "r1l",
        "download",
        request=MockRequest(),
    )

    current_items = [item for item in items if item["current"]]
    assert current_items == [
        {
            "text": "Download data",
            "href": "/start_download/r1l",
            "current": True,
        }
    ]
