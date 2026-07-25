import logging

# import requests
import yaml

from src.utils import get_config_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sync_teams_and_workspaces():
    """
    Idempotent function to reconcile Teams and Workspaces in Sigma.
    Reads RBAC state from deploy/{env}/teams.yaml and deploy/{env}/workspaces.yaml.
    """
    # headers = get_sigma_headers()

    # 1. Sync Teams
    teams_path = get_config_path("teams.yaml")
    with open(teams_path, "r") as file:
        teams_config = yaml.safe_load(file)

    logger.info("Fetching existing teams from API...")
    # Mocking GET /teams
    existing_teams = {"Data Engineering": "team-id-abc"}

    for team in teams_config.get("teams", []):
        team_name = team["name"]

        # Idempotency Check
        if team_name in existing_teams:
            logger.info(f"Team '{team_name}' exists. Reconciling members...")
            # Perform GET /teams/{id}/members and compare with team["members"]
            # Add missing members via POST, remove extra members via DELETE
        else:
            logger.info(f"Team '{team_name}' does not exist. Creating team...")
            # Perform POST /teams
            # Then POST /teams/{id}/members to add the users

    # 2. Sync Workspaces
    ws_path = get_config_path("workspaces.yaml")
    with open(ws_path, "r") as file:
        ws_config = yaml.safe_load(file)

    logger.info("Fetching existing workspaces from API...")
    # Mocking GET /workspaces
    existing_workspaces = {"Core Reporting": "ws-id-xyz"}

    for ws in ws_config.get("workspaces", []):
        ws_name = ws["name"]

        if ws_name in existing_workspaces:
            logger.info(f"Workspace '{ws_name}' exists. Reconciling permissions...")
            # Fetch workspace permissions and sync with ws["permissions"] (Editor/Viewer)
        else:
            logger.info(f"Workspace '{ws_name}' does not exist. Creating workspace...")
            # POST /workspaces
            # Then POST /workspaces/{id}/grants for permissions


if __name__ == "__main__":
    sync_teams_and_workspaces()
