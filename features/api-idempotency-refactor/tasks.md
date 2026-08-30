# Implementation Tasks: API Idempotency & Workflow Refactor

## Phase 1: Foundation (API Client & Contracts)
- [ ] **Task 1: Define API Contracts**
  - Create `src/utils/api_contracts.py`.
  - Define `Team`, `Workspace`, and `WorkspaceCreateRequest` using `typing.TypedDict` or `@dataclass`.
- [ ] **Task 2: Upgrade API Client**
  - Modify `src/utils/api_client.py`.
  - Add `requests` and `urllib3.util.retry` dependencies (ensure `requests` is in the project dependencies if not already).
  - Implement a session with `Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])`.
  - Implement a mock authentication handler that retrieves a token using `SIGMA_CLIENT_ID` and sets the `Authorization: Bearer <token>` header.

## Phase 2: Idempotency Enforcement in Sync Scripts
- [ ] **Task 3: Refactor `sync_rbac.py` - Teams**
  - Replace `# Mocking GET /teams` with an actual `session.get(f"{SIGMA_API_URL}/teams")`.
  - Implement the "Read -> Diff -> Apply" logic. Log when a team is skipped due to idempotency.
  - Replace `# POST /teams` with actual API calls using the defined data contracts.
- [ ] **Task 4: Refactor `sync_rbac.py` - Workspaces**
  - Replace `# Mocking GET /workspaces` with an actual `session.get(f"{SIGMA_API_URL}/workspaces")`.
  - Implement idempotency checks and actual `POST /workspaces` logic.

## Phase 3: PR Workspace Lifecycle
- [ ] **Task 5: Refactor `manage_pr_workspace.py` - Create**
  - Implement `GET /workspaces?search=PR-{pr_id}` to check for existence (collision avoidance).
  - Implement `POST /workspaces` using the `WorkspaceCreateRequest` contract.
- [ ] **Task 6: Refactor `manage_pr_workspace.py` - Teardown**
  - Implement `GET /workspaces?search=PR-{pr_id}` to find the workspace ID.
  - Implement `DELETE /workspaces/{id}` to safely tear down the environment.