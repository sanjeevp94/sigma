# Spec-Driven Development (SDD) Suggestions

Based on a review of the `sigma-bi-as-code` repository, here are key areas and updates that would significantly benefit from adopting Spec-Driven Development (using GitHub Spec Kit). The SDD workflow will help formally document requirements and API contracts before implementation, aligning perfectly with the declarative GitOps principles of the project.

## 1. Formalize Sigma REST API Integrations

**Issue:** Currently, scripts like `src/sync_rbac.py` and `src/sync_connections.py` have placeholders or "mocking" for Sigma API calls (e.g., `# Mocking GET /teams`).

**Benefit of SDD:**
- **Contract Definition:** By using `/speckit.specify`, you can explicitly define the JSON request/response payloads required by the Sigma v2 REST API (e.g., what the `POST /teams/{id}/members` request should look like).
- **Error Handling:** A spec can dictate how scripts must gracefully handle API rate limits (HTTP 429) and authentication expirations.
- **Recommendation:** Create a spec `specs/api-integration-spec.md` to map out the exact HTTP methods, endpoints, and error handling for `sync_rbac.py` and `sync_connections.py` before fully implementing the Python logic.

## 2. Enforce Idempotency Rules

**Issue:** The `ARCHITECTURE.md` strictly mandates idempotency for all Python sync scripts.

**Benefit of SDD:**
- **Testable Criteria:** Specifications allow you to define acceptance criteria for idempotency (e.g., "Running the script twice with no configuration changes must result in 0 POST/PUT/DELETE API calls").
- **Recommendation:** Use `/speckit.plan` to outline the logic for idempotency checks (fetching current state -> comparing -> applying delta) across all sync scripts (`sync_artifacts.py`, `sync_tags.py`, `sync_rbac.py`).

## 3. Strict Infrastructure Validation (Graviton Enforcment)

**Issue:** Redshift connections must enforce Graviton (rg) clusters and reject RA3.

**Benefit of SDD:**
- **Validation Logic:** A spec can clearly define the validation logic and the expected failure behavior if an invalid configuration is pushed to the `deploy/{env}/connections.yaml` file.
- **Recommendation:** Create a spec specifically for `src/sync_connections.py` focusing on connection string parsing and validation against the allowed instance types.

## 4. PR Workspace Management Lifecycle

**Issue:** The script `manage_pr_workspace.py` likely handles temporary resources.

**Benefit of SDD:**
- **Lifecycle Definition:** A specification can document the exact lifecycle (Create on PR open -> Update on PR commit -> Tear down on PR merge/close) and the specific naming conventions required to avoid collisions between developers.
- **Recommendation:** Implement a spec detailing the GitHub Actions/Jenkins CI triggers and the required CLI arguments for `manage_pr_workspace.py`.

By incorporating Spec-Driven Development into these areas, the team can ensure that the "BI-as-Code" infrastructure remains predictable, robust, and explicitly documented *before* code is written.