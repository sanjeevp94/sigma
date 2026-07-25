import logging

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
    # headers = get_sigma_headers()

    tags_path = get_config_path("tags.yaml")
    with open(tags_path, "r") as file:
        tags_config = yaml.safe_load(file)

    for tag_def in tags_config.get("tags", []):
        tag_name = tag_def["name"]

        logger.info(f"Reconciling targets for Tag: '{tag_name}'")

        for target in tag_def.get("targets", []):
            artifact_type = target["artifact_type"]
            artifact_name = target["artifact_name"]
            version = target["version"]

            logger.info(f"Looking up ID for {artifact_type} '{artifact_name}' to apply tag.")
            # Mock looking up the artifact ID and its latest version number
            # artifact_id = "mock-id-123"
            latest_version = 42  # example version retrieved from API

            target_version = latest_version if version == "latest" else int(version)

            # Idempotency: Get current tag state
            # response = requests.get(f"{SIGMA_API_URL}/tags/{tag_name}", headers=headers)
            current_tagged_version = 41  # mock current tagged version

            if current_tagged_version != target_version:
                logger.info(f"Updating {tag_name} tag for {artifact_name} to version {target_version}")
                # POST /tags/{tag_name}/apply
                # payload = {"artifactId": artifact_id, "version": target_version}
            else:
                logger.info(f"Tag {tag_name} is already pointing to version {target_version}. No action needed.")


if __name__ == "__main__":
    sync_tags()
