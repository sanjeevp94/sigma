import argparse
import logging
import sys

from src.utils.api_client import get_sigma_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_pr_workspace(pr_id: str):
    """
    Creates an ephemeral workspace for a PR.
    """
    get_sigma_client()
    ws_name = f"PR-{pr_id}"

    logger.info(f"Creating ephemeral workspace: {ws_name}")
    # In a real environment, you would use the Sigma API to create the workspace.
    # response = session.post(f"{SIGMA_API_URL}/workspaces", json={"name": ws_name})
    # response.raise_for_status()
    # ws_id = response.json().get("workspaceId")

    ws_id = f"mock-ws-{pr_id}"
    logger.info(f"Workspace {ws_name} created with ID: {ws_id}")

    # You would then typically call your artifact sync logic here,
    # injecting the ws_id so the artifacts are pushed into this specific workspace.
    # We will simulate this for the stub.
    logger.info(f"Deploying PR artifacts to workspace {ws_id}...")


def teardown_pr_workspace(pr_id: str):
    """
    Tears down an ephemeral workspace for a PR.
    """
    get_sigma_client()
    ws_name = f"PR-{pr_id}"

    logger.info(f"Looking up workspace: {ws_name}")
    # response = session.get(f"{SIGMA_API_URL}/workspaces?search={ws_name}")
    # response.raise_for_status()
    # existing_workspaces = response.json().get("entries", [])

    # Mock finding it
    existing_workspaces = [{"workspaceId": f"mock-ws-{pr_id}", "name": ws_name}]

    if existing_workspaces:
        ws_id = existing_workspaces[0]["workspaceId"]
        logger.info(f"Tearing down ephemeral workspace ID: {ws_id}")
        # response = session.delete(f"{SIGMA_API_URL}/workspaces/{ws_id}")
        # response.raise_for_status()
        logger.info(f"Successfully deleted workspace {ws_name}")
    else:
        logger.warning(f"No workspace found for {ws_name}. Skipping teardown.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Ephemeral PR Workspaces in Sigma.")
    parser.add_argument("--pr-id", type=str, required=True, help="The Pull Request ID (e.g., PR-123)")
    parser.add_argument("--action", choices=["create", "teardown"], required=True, help="Action to perform")

    args = parser.parse_args()

    if args.action == "create":
        create_pr_workspace(args.pr_id)
    elif args.action == "teardown":
        teardown_pr_workspace(args.pr_id)
    else:
        logger.error(f"Invalid action: {args.action}")
        sys.exit(1)
