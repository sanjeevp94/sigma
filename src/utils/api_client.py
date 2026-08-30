import logging
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

SIGMA_API_URL = os.environ.get("SIGMA_API_URL", "https://api.sigmacomputing.com/v2")


def get_sigma_client() -> requests.Session:
    """
    Returns a configured requests Session object with retry logic and authentication headers.
    """
    client_id = os.environ.get("SIGMA_CLIENT_ID")
    client_secret = os.environ.get("SIGMA_CLIENT_SECRET")

    if not client_id or not client_secret:
        logger.warning(
            "SIGMA_CLIENT_ID or SIGMA_CLIENT_SECRET not set. Proceeding without auth (for local mock testing)."
        )
        # In a real scenario, this would raise an error or exit.
        token = "mock_token"  # nosec B105
    else:
        # We would typically do this to get a bearer token
        response = requests.post(
            f"{SIGMA_API_URL}/auth/token",
            data={"client_id": client_id, "client_secret": client_secret},
            timeout=10,
        )
        response.raise_for_status()
        token = response.json()["access_token"]

    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update(
        {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"}
    )

    return session
