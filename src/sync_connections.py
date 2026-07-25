import logging
import os

# import requests
import yaml

from src.utils import get_config_path
from src.utils.api_client import SIGMA_API_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sync_connections():
    """
    Idempotent function to reconcile Redshift connections in Sigma.
    Reads connection state from deploy/{env}/connections.yaml.
    """
    env = os.environ.get("DEPLOY_ENV", "dev").upper()

    # Normally credentials should be fetched from Jenkins, e.g. REDSHIFT_DEV_PASS
    os.environ.get(f"REDSHIFT_{env}_PASS", "dummy_pass")

    config_path = get_config_path("connections.yaml")
    if not os.path.exists(config_path):
        logger.error(f"Configuration file not found: {config_path}")
        return

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # headers = get_sigma_headers()

    # Mocking the GET request to retrieve existing connections to demonstrate idempotency
    logger.info(f"Fetching existing connections from {SIGMA_API_URL}/connections")

    # response = requests.get(f"{SIGMA_API_URL}/connections", headers=headers)
    # response.raise_for_status()
    # existing = {c["name"]: c["connectionId"] for c in response.json().get("entries", [])}

    existing = {"redshift-prod": "existing-conn-id-123"}  # Mock state

    for conn in config.get("connections", []):
        name = conn["name"]
        # payload = {
        #     "name": name,
        #     "type": conn["type"],
        #     "host": conn["properties"]["host"],
        #     "port": conn["properties"]["port"],
        #     "database": conn["properties"]["database"],
        #     "user": conn["properties"]["user"],
        #     "password": db_password,
        # }

        # Idempotency Check: if connection exists, PUT; otherwise POST
        if name in existing:
            logger.info(f"Connection '{name}' exists. Updating via PUT.")
            # requests.put(f"{SIGMA_API_URL}/connections/{existing[name]}", headers=headers, json=payload)
        else:
            logger.info(f"Connection '{name}' does not exist. Creating via POST.")
            # requests.post(f"{SIGMA_API_URL}/connections", headers=headers, json=payload)


if __name__ == "__main__":
    sync_connections()
