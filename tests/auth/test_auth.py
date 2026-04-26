import urllib.parse
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from unittest.mock import MagicMock, patch

from mavis.reporting.helpers.auth_helper import log_user_in
from tests.helpers import mock_user_info


def default_url():
    return "/reports/team/r1l/vaccinations"


def it_redirects_to_mavis_start(response):
    # Check that the response had a redirect code.
    assert response.status_code == HTTPStatus.FOUND
    redirect_to = response.headers["Location"]
    assert redirect_to.startswith("http://mavis.test/")
    assert "/start" in redirect_to
    # Check that the return_url param is on the redirect
    parsed_url = urllib.parse.urlparse(redirect_to)
    assert "redirect_uri=" in parsed_url.query
    return True


def test_when_session_has_a_user_id_and_is_not_expired_it_does_not_redirect(
    app, client
):
    with app.app_context():
        with client.session_transaction() as session:
            log_user_in(mock_user_info(), session)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "cohort": 546,
            "vaccinated": 456,
            "not_vaccinated": 90,
            "vaccinations_given": {"school_count": 350, "community_count": 52},
            "consent_given": 400,
            "no_consent": 146,
            "consent_no_response": 100,
            "consent_refused": 30,
            "consent_conflicts": 16,
            "consent_refusal_reasons": {
                "contains_gelatine": 1,
                "already_vaccinated": 8,
                "will_be_vaccinated_elsewhere": 5,
                "medical_reasons": 3,
                "personal_choice": 12,
                "other": 1,
            },
            "consent_routes": {
                "website": 320,
                "phone": 45,
                "paper": 22,
                "in_person": 10,
                "self_consent": 3,
            },
            "monthly_vaccinations_given": [
                {
                    "month": "September",
                    "year": 2025,
                    "school_count": 121,
                    "community_count": 0,
                },
                {
                    "month": "October",
                    "year": 2025,
                    "school_count": 145,
                    "community_count": 0,
                },
                {
                    "month": "November",
                    "year": 2025,
                    "school_count": 136,
                    "community_count": 0,
                },
            ],
        }

        with patch(
            "mavis.reporting.helpers.mavis_helper.api_call",
            return_value=mock_response,
        ):
            response = client.get(default_url())
            assert response.status_code == HTTPStatus.OK


def test_when_session_has_a_user_id_but_is_expired_it_redirects_to_mavis_start(client):
    with client.session_transaction() as session:
        # set session vars without going through the login route
        session["user_id"] = 1
        session["last_visit"] = datetime.now().astimezone(timezone.utc) - timedelta(
            hours=101
        )

    response = client.get(default_url())
    assert it_redirects_to_mavis_start(response)


def test_when_user_id_not_in_session_it_redirects_to_mavis_sign_in(client):
    with client.session_transaction() as session:
        # set user_id session var without going through the login route
        session["user_id"] = None

    response = client.get(default_url(), follow_redirects=False)
    assert it_redirects_to_mavis_start(response)


def test_when_api_returns_401_with_stale_session_it_redirects_to_mavis_start(
    app, client
):
    with app.app_context():
        with client.session_transaction() as session:
            log_user_in(mock_user_info(), session)

        mock_response = MagicMock()
        mock_response.status_code = HTTPStatus.UNAUTHORIZED
        mock_response.is_success = False

        with patch(
            "mavis.reporting.helpers.mavis_helper.get_request",
            return_value=mock_response,
        ):
            response = client.get(default_url())
            assert it_redirects_to_mavis_start(response)
