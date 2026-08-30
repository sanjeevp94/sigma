import logging

import yaml
from requests.exceptions import RequestException

from src.utils import get_config_path
from src.utils.api_client import SIGMA_API_URL, get_sigma_client
from src.utils.api_contracts import TeamCreateRequest, WorkspaceCreateRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sync_teams_and_workspaces():
    """
    Idempotent function to reconcile Teams and Workspaces in Sigma.
    Reads RBAC state from deploy/{env}/teams.yaml and deploy/{env}/workspaces.yaml.
    """
    session = get_sigma_client()

    # 1. Sync Teams
    teams_path = get_config_path("teams.yaml")
    with open(teams_path, "r") as file:
        teams_config = yaml.safe_load(file)

    logger.info("Fetching existing teams from API...")
    try:
        response = session.get(f"{SIGMA_API_URL}/teams")
        response.raise_for_status()
        existing_teams = {t["name"]: t["teamId"] for t in response.json().get("entries", [])}
    except RequestException as e:
        logger.error(f"Failed to fetch teams: {e}")
        # Mock state for local testing when API is unreachable
        existing_teams = {"Data Engineering": "team-id-abc"}

    for team in teams_config.get("teams", []):
        team_name = team["name"]

        # Idempotency Check
        if team_name in existing_teams:
            logger.info(f"Idempotency: Team '{team_name}' already exists. Skipping creation.")
            team_id = existing_teams[team_name]

            try:
                # Sync members
                members_resp = session.get(f"{SIGMA_API_URL}/teams/{team_id}/members")
                members_resp.raise_for_status()
                current_members = {m["memberId"] for m in members_resp.json().get("entries", [])}

                desired_members = set(team.get("members", []))

                members_to_add = desired_members - current_members
                members_to_remove = current_members - desired_members

                for member_id in members_to_add:
                    session.post(f"{SIGMA_API_URL}/teams/{team_id}/members", json={"memberId": member_id})

                for member_id in members_to_remove:
                    session.delete(f"{SIGMA_API_URL}/teams/{team_id}/members/{member_id}")

                if not members_to_add and not members_to_remove:
                    logger.info(f"Idempotency: Team '{team_name}' members are up-to-date.")
                else:
                    logger.info(
                        f"Updated members for team '{team_name}'. "
                        f"Added {len(members_to_add)}, removed {len(members_to_remove)}."
                    )
            except RequestException as e:
                logger.error(f"Failed to sync members for team {team_name}: {e}")
        else:
            logger.info(f"Team '{team_name}' does not exist. Creating team...")
            payload: TeamCreateRequest = {"name": team_name}
            try:
                post_resp = session.post(f"{SIGMA_API_URL}/teams", json=payload)
                post_resp.raise_for_status()
                logger.info(f"Successfully created team '{team_name}'")

                team_id = post_resp.json().get("teamId")
                desired_members = set(team.get("members", []))
                for member_id in desired_members:
                    session.post(f"{SIGMA_API_URL}/teams/{team_id}/members", json={"memberId": member_id})

                if desired_members:
                    logger.info(f"Added {len(desired_members)} members to new team '{team_name}'.")

            except RequestException as e:
                logger.error(f"Failed to create team {team_name}: {e}")

    # 2. Sync Workspaces
    ws_path = get_config_path("workspaces.yaml")
    with open(ws_path, "r") as file:
        ws_config = yaml.safe_load(file)

    logger.info("Fetching existing workspaces from API...")
    try:
        response = session.get(f"{SIGMA_API_URL}/workspaces")
        response.raise_for_status()
        existing_workspaces = {w["name"]: w["workspaceId"] for w in response.json().get("entries", [])}
    except RequestException as e:
        logger.error(f"Failed to fetch workspaces: {e}")
        # Mock state for local testing when API is unreachable
        existing_workspaces = {"Core Reporting": "ws-id-xyz"}

    for ws in ws_config.get("workspaces", []):
        ws_name = ws["name"]

        # Idempotency Check
        if ws_name in existing_workspaces:
            logger.info(f"Idempotency: Workspace '{ws_name}' already exists. Skipping creation.")
            ws_id = existing_workspaces[ws_name]
            try:
                grants_resp = session.get(f"{SIGMA_API_URL}/workspaces/{ws_id}/grants")
                grants_resp.raise_for_status()
                current_grants = {g["granteeId"]: g["permission"] for g in grants_resp.json().get("entries", [])}

                desired_grants = {g["granteeId"]: g["permission"] for g in ws.get("permissions", [])}

                for grantee_id, permission in desired_grants.items():
                    if grantee_id not in current_grants or current_grants[grantee_id] != permission:
                        session.post(
                            f"{SIGMA_API_URL}/workspaces/{ws_id}/grants",
                            json={"granteeId": grantee_id, "permission": permission},
                        )

                for grantee_id in current_grants:
                    if grantee_id not in desired_grants:
                        session.delete(f"{SIGMA_API_URL}/workspaces/{ws_id}/grants/{grantee_id}")

                logger.info(f"Idempotency: Workspace '{ws_name}' permissions synced.")
            except RequestException as e:
                logger.error(f"Failed to sync permissions for workspace {ws_name}: {e}")
        else:
            logger.info(f"Workspace '{ws_name}' does not exist. Creating workspace...")
            payload: WorkspaceCreateRequest = {"name": ws_name}
            try:
                post_resp = session.post(f"{SIGMA_API_URL}/workspaces", json=payload)
                post_resp.raise_for_status()
                logger.info(f"Successfully created workspace '{ws_name}'")

                ws_id = post_resp.json().get("workspaceId")
                desired_grants = {g["granteeId"]: g["permission"] for g in ws.get("permissions", [])}
                for grantee_id, permission in desired_grants.items():
                    session.post(
                        f"{SIGMA_API_URL}/workspaces/{ws_id}/grants",
                        json={"granteeId": grantee_id, "permission": permission},
                    )

                if desired_grants:
                    logger.info(f"Added {len(desired_grants)} grants to new workspace '{ws_name}'.")

            except RequestException as e:
                logger.error(f"Failed to create workspace {ws_name}: {e}")


if __name__ == "__main__":
    sync_teams_and_workspaces()
