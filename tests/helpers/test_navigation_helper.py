import json
from urllib.parse import quote_plus

import pytest
from flask import Flask

from mavis.reporting.helpers import navigation_helper
from tests.conftest import MockRequest


@pytest.fixture()
def app():
    return Flask(__name__)


def reporting_context_cookie(*, navigation_items=None):
    payload = {}
    if navigation_items is not None:
        payload["navigation_items"] = navigation_items

    return quote_plus(json.dumps(payload))


def test_build_navigation_items_uses_reporting_context_navigation_items():
    items = navigation_helper.build_navigation_items(
        MockRequest(
            cookies={
                "mavis_reporting_context": reporting_context_cookie(
                    navigation_items=[
                        {"title": "Schools", "path": "/schools"},
                        {
                            "title": "Unmatched responses",
                            "path": "/consent-forms",
                            "count": 135,
                        },
                    ]
                )
            }
        )
    )

    assert items[0] == {"href": "/schools", "text": "Schools"}
    assert items[1]["href"] == "/consent-forms"
    assert items[1]["classes"] == "app-header__navigation-item--with-count"
    assert "Unmatched responses" in str(items[1]["html"])
    assert "135" in str(items[1]["html"])


def test_build_navigation_items_falls_back_without_reporting_context_cookie():
    items = navigation_helper.build_navigation_items(MockRequest())

    assert [item["href"] for item in items] == [
        "/schools",
        "/patients",
        "/sessions",
        "/vaccines",
        "/consent-forms",
        "/school-moves",
        "/reports",
        "/imports",
        "/team",
    ]
