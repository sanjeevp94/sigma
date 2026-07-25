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
    # session = get_sigma_client()

    # We append the GIT_COMMIT to the payload description or metadata so it can be tracked deterministically later
    git_commit = os.environ.get("GIT_COMMIT", "unknown")

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

                # Append git commit tracking to the description
                original_desc = payload.get("description", "")
                payload["description"] = f"{original_desc} [GIT_COMMIT: {git_commit}]"

                # In a real scenario, you'd map the file to a known workbookId via state or API lookup.
                # E.g. GET /workbooks?search={artifact_name}
                logger.info(f"Looking up existing ID for {artifact_type}: '{artifact_name}'")

                existing_id = "mock-id-123"  # Mock finding the artifact

                if existing_id:
                    logger.info(f"Artifact found. PUT for '{artifact_name}' with hash {git_commit}")
                    # session.put(f"{SIGMA_API_URL}/{artifact_type}/{existing_id}", json=payload)
                else:
                    logger.info(f"Artifact not found. POST for '{artifact_name}' with hash {git_commit}")
                    # session.post(f"{SIGMA_API_URL}/{artifact_type}", json=payload)


if __name__ == "__main__":
    sync_artifacts()
