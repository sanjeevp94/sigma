from typing import TypedDict


class WorkspaceCreateRequest(TypedDict):
    name: str


class Workspace(TypedDict):
    workspaceId: str
    name: str


class TeamCreateRequest(TypedDict):
    name: str


class Team(TypedDict):
    teamId: str
    name: str


class TeamMemberCreateRequest(TypedDict):
    userId: str


class WorkspaceGrantCreateRequest(TypedDict):
    granteeId: str
    granteeType: str  # "team" or "user"
    permission: str  # "viewer", "explorer", "creator", "admin"
