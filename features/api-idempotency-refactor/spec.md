# Feature Specification: API Idempotency & Workflow Refactor

## 1. Problem Statement
The current Python execution scripts in `src/` utilize mocked endpoints and placeholder logic for Sigma API interactions. Additionally, while the architecture mandates idempotency, the specific mechanisms for enforcing it are not formally codified across all scripts. The PR workspace management lifecycle also lacks a formal data contract and error-handling framework. This refactor bridges the gap between the theoretical GitOps architecture and the actual implementation.

## 2. Requirements

### 2.1 Formalized API Integrations & Data Contracts
- **Data Contracts:** All payloads sent to and received from the Sigma v2 REST API must adhere to a strict data contract. We will define these contracts using explicit JSON schema definitions or Python dataclasses/typing within `src/utils/api_contracts.py`.
- **API Client Standardization:** `src/utils/api_client.py` must handle authentication (using `SIGMA_CLIENT_ID` and `SIGMA_CLIENT_SECRET`), token expiration, and HTTP 429 rate limit retries transparently.

### 2.2 Strict Idempotency Enforcement
- All sync scripts (`sync_rbac.py`, `sync_artifacts.py`, `sync_tags.py`) must follow a strict "Read -> Diff -> Apply" pattern.
- The scripts must log the delta before applying it. If there is no delta (the desired state matches the current API state), the script must exit successfully with 0 mutating API calls (POST, PUT, DELETE).

### 2.3 PR Workspace Management Lifecycle
- `manage_pr_workspace.py` must strictly implement the following lifecycle:
  - **Create:** Triggered on PR open. Creates a workspace named `PR-{pr_id}`.
  - **Update:** (Simulated by running the artifact sync scripts targeting this workspace).
  - **Teardown:** Triggered on PR close/merge. Finds `PR-{pr_id}` and deletes it.
- **Collision Avoidance:** The script must handle the scenario where a `Create` event fires but the workspace already exists (e.g., failed teardown previously). It should log a warning, reset the workspace contents, and proceed without failing.

### 2.4 Exclusions
- Changes to the Redshift Graviton (rg) validation in `sync_connections.py` are explicitly excluded from this iteration.

## 3. Acceptance Criteria
1. **API Mocks Removed:** All `# Mocking GET /...` comments in `sync_rbac.py` and `manage_pr_workspace.py` are replaced with actual calls using the centralized `api_client`.
2. **Idempotency Verified:** Running `sync_rbac.py` twice consecutively with the same `teams.yaml` and `workspaces.yaml` results in API mutating calls only on the first run. The second run logs that no changes are necessary.
3. **Data Contracts Configured:** A new file `src/utils/api_contracts.py` exists and is used by the sync scripts to validate payloads before dispatching API requests.
4. **Resilient Workspace Management:** `manage_pr_workspace.py --action create --pr-id 123` succeeds even if the workspace `PR-123` already exists.