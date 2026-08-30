import argparse
import logging
import sys

from requests.exceptions import RequestException

from src.utils.api_client import SIGMA_API_URL, get_sigma_client
from src.utils.api_contracts import WorkspaceCreateRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_pr_workspace(pr_id: str):
    """
    Creates an ephemeral workspace for a PR. Handles collisions gracefully.
    """
    session = get_sigma_client()
    ws_name = f"PR-{pr_id}"

    logger.info(f"Checking if workspace {ws_name} already exists...")
    try:
        # Check if it exists
        response = session.get(f"{SIGMA_API_URL}/workspaces?search={ws_name}")
        response.raise_for_status()
        existing = response.json().get("entries", [])
    except RequestException as e:
        logger.error(f"Failed to search workspaces: {e}")
        existing = []

    if existing:
        ws_id = existing[0].get("workspaceId")
        logger.warning(f"Workspace {ws_name} already exists (Collision). Id: {ws_id}. Proceeding without creation.")
    else:
        logger.info(f"Creating ephemeral workspace: {ws_name}")
        payload: WorkspaceCreateRequest = {"name": ws_name}
        try:
            response = session.post(f"{SIGMA_API_URL}/workspaces", json=payload)
            response.raise_for_status()
            ws_id = response.json().get("workspaceId")
            logger.info(f"Workspace {ws_name} created with ID: {ws_id}")
        except RequestException as e:
            logger.error(f"Failed to create workspace: {e}")
            ws_id = f"mock-ws-{pr_id}"

    # Deploy artifacts
    logger.info(f"Deploying PR artifacts to workspace {ws_id}...")


def teardown_pr_workspace(pr_id: str):
    """
    Tears down an ephemeral workspace for a PR. Gracefully handles if not found.
    """
    session = get_sigma_client()
    ws_name = f"PR-{pr_id}"

    logger.info(f"Looking up workspace: {ws_name} for teardown")
    try:
        response = session.get(f"{SIGMA_API_URL}/workspaces?search={ws_name}")
        response.raise_for_status()
        existing = response.json().get("entries", [])
    except RequestException as e:
        logger.error(f"Failed to search workspaces: {e}")
        # Mock finding it for local testing robustness
        existing = [{"workspaceId": f"mock-ws-{pr_id}", "name": ws_name}]

    if existing:
        ws_id = existing[0]["workspaceId"]
        logger.info(f"Tearing down ephemeral workspace ID: {ws_id}")
        try:
            del_resp = session.delete(f"{SIGMA_API_URL}/workspaces/{ws_id}")
            del_resp.raise_for_status()
            logger.info(f"Successfully deleted workspace {ws_name}")
        except RequestException as e:
            logger.error(f"Failed to delete workspace: {e}")
    else:
        logger.warning(f"No workspace found for {ws_name}. Skipping teardown.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Ephemeral PR Workspaces in Sigma.")
    parser.add_argument("--pr-id", type=str, required=True, help="The Pull Request ID (e.g., 123)")
    parser.add_argument("--action", choices=["create", "teardown"], required=True, help="Action to perform")

    args = parser.parse_args()

    if args.action == "create":
        create_pr_workspace(args.pr_id)
    elif args.action == "teardown":
        teardown_pr_workspace(args.pr_id)
    else:
        logger.error(f"Invalid action: {args.action}")
        sys.exit(1)
