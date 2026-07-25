import logging
import os

# import requests
import yaml

from src.utils import get_config_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sync_tags():
    """
    Idempotent function to update Sigma version tags based on the active environment (UAT or PROD).
    Reads tag mapping state from deploy/{env}/tags.yaml.
    """
    # session = get_sigma_client()

    # We retrieve the GIT_COMMIT to use deterministic versioning where applicable.
    git_commit = os.environ.get("GIT_COMMIT", "latest")

    tags_path = get_config_path("tags.yaml")
    with open(tags_path, "r") as file:
        tags_config = yaml.safe_load(file)

    for tag_def in tags_config.get("tags", []):
        tag_name = tag_def["name"]

        logger.info(f"Reconciling targets for Tag: '{tag_name}'")

        for target in tag_def.get("targets", []):
            target["artifact_type"]
            artifact_name = target["artifact_name"]

            # Use deterministic GIT_COMMIT if the config explicitly specifies it
            version_directive = target.get("version", "latest")
            version = git_commit if version_directive == "GIT_COMMIT" else version_directive

            logger.info(f"Looking up ID for {artifact_name} with directive: {version}")

            # In reality, if version is a git commit hash, we would query the Sigma API for the workbook history
            # and find the version ID that corresponds to the description matching the hash.
            # GET /workbooks/{id}/versions
            # artifact_id = "mock-id-123"

            # We mock the resolved version.
            target_version = 42 if version in ["latest", git_commit] else int(version)

            # Idempotency: Get current tag state
            # response = session.get(f"{SIGMA_API_URL}/tags/{tag_name}")
            current_tagged_version = 41  # mock current tagged version

            if current_tagged_version != target_version:
                logger.info(f"Updating {tag_name} tag to version {target_version} (directive: {version})")
                # session.post(f"/tags/{tag_name}/apply", json={"artifactId": artifact_id, "version": target_version})
            else:
                logger.info(f"Tag {tag_name} is already pointing to version {target_version}. No action needed.")


if __name__ == "__main__":
    sync_tags()
