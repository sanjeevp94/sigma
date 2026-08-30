# Technical Plan: API Idempotency & Workflow Refactor

## 1. Scope
This plan details the technical implementation required to satisfy `spec.md`. We will refactor `src/utils/api_client.py` to be robust, introduce `src/utils/api_contracts.py` for data validation, and update `src/sync_rbac.py` and `src/manage_pr_workspace.py` to utilize these standardizations while strictly enforcing idempotency.

## 2. Technical Design

### 2.1 API Client Standardization (`src/utils/api_client.py`)
- We will replace the current rudimentary implementation (or stub) with a `requests.Session` object configured with a `urllib3.util.retry.Retry` strategy.
- **Retry Strategy:**
  - Backoff factor: 1
  - Status forcelist: `[429, 500, 502, 503, 504]`
  - Total retries: 3
- The `get_sigma_client()` function will return this configured session.
- Authentication will be handled by fetching a bearer token via the `/auth/token` endpoint using `SIGMA_CLIENT_ID` and `SIGMA_CLIENT_SECRET`, attaching it to the session headers.

### 2.2 Data Contracts (`src/utils/api_contracts.py`)
- Since Python >=3.11 is used, we will utilize `dataclasses` (or raw `TypedDict` for simplicity without adding third-party deps like `pydantic`) to enforce the shape of the data.
- **Contracts to define:**
  - `Team`: `{ "teamId": str, "name": str }`
  - `Workspace`: `{ "workspaceId": str, "name": str }`
  - `WorkspaceCreateRequest`: `{ "name": str }`

### 2.3 Refactoring `src/sync_rbac.py`
- **Current State:** Mocks GET requests and prints actions.
- **Proposed State:**
  - `GET /teams`: Fetch current teams, parsing into a dictionary of `{name: id}`.
  - Diff against `deploy/{env}/teams.yaml`.
  - For missing teams: `POST /teams` with payload `{"name": "..."}`.
  - Log when a team already exists and skip creation.
  - Similarly, implement `GET /workspaces` and `POST /workspaces` using the `Read -> Diff -> Apply` logic.

### 2.4 Refactoring `src/manage_pr_workspace.py`
- **Current State:** Contains commented out `requests.post` and mocks finding the workspace.
- **Proposed State:**
  - **Create Action:**
    - Perform a `GET /workspaces` (or `GET /workspaces?search=PR-{pr_id}`).
    - If found: Log a warning (collision detected), and optionally clear its contents (if API permits easily, or simply proceed as it might be a retry). We will just log the warning and proceed.
    - If not found: `POST /workspaces` with `WorkspaceCreateRequest`.
  - **Teardown Action:**
    - Perform `GET /workspaces?search=PR-{pr_id}`.
    - If found: Extract `workspaceId` and perform `DELETE /workspaces/{id}`.
    - If not found: Log a warning and exit successfully.

## 3. Testing Strategy
- We will utilize `make lint` (ruff) and `make security` (bandit) to ensure the newly written code adheres to project standards.
- (Manual Validation): Since we lack a live Sigma environment to test against in this sandbox, we will ensure the Python logic correctly handles the request construction and mock responses appropriately if we write unit tests, or ensure the code logic is visibly correct and relies on standard `requests` behavior.