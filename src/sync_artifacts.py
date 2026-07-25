import json
import logging
import os

# import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sync_artifacts():
    """
    Idempotent function to push JSON payload definitions (workbooks/data_models) to Sigma.
    This script is typically only run on the main branch (UAT) to increment the version.
    """
    # headers = get_sigma_headers()

    artifact_dirs = {"workbooks": "artifacts/workbooks", "data_models": "artifacts/data_models"}

    for artifact_type, dir_path in artifact_dirs.items():
        if not os.path.exists(dir_path):
            continue

        for filename in os.listdir(dir_path):
            if filename.endswith(".json"):
                file_path = os.path.join(dir_path, filename)
                with open(file_path, "r") as f:
                    payload = json.load(f)

                artifact_name = payload.get("name")

                # In a real scenario, you'd map the file to a known workbookId via state or API lookup.
                # E.g. GET /workbooks?search={artifact_name}
                logger.info(f"Looking up existing ID for {artifact_type}: '{artifact_name}'")

                existing_id = "mock-id-123"  # Mock finding the artifact

                if existing_id:
                    logger.info(f"Artifact found. Pushing new version (PUT) for '{artifact_name}'...")
                    # requests.put(f"{SIGMA_API_URL}/{artifact_type}/{existing_id}", headers=headers, json=payload)
                else:
                    logger.info(f"Artifact not found. Creating new (POST) for '{artifact_name}'...")
                    # requests.post(f"{SIGMA_API_URL}/{artifact_type}", headers=headers, json=payload)


if __name__ == "__main__":
    sync_artifacts()
