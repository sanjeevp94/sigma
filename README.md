# Sigma BI-as-Code

This repository manages the Business Intelligence environment using a strictly version-controlled, GitOps-managed infrastructure utilizing the Sigma v2 REST API.

## Core Concepts

*   **Bitbucket is the source of truth.** Manual UI changes will be overwritten.
*   **RBAC and Workspaces** are declarative and defined in `deploy/`.
*   **Infrastructure (Redshift)** enforces Graviton instance types.
*   **API Idempotency:** Sync scripts enforce a strict Read -> Diff -> Apply cycle utilizing explicit JSON data contracts (`src/utils/api_contracts.py`) and a resilient REST client (`src/utils/api_client.py`).

## Spec-Driven Development (SDD)
This repository leverages GitHub Spec Kit to document feature architecture, API integrations, and idempotency rules prior to implementation.
- Project specifications are written inside `features/` or `specs/`.
- Important architectural rules and REST API definitions are indexed in the `wiki/`.

## Development Setup

We use `uv` for ultra-fast python environments.

1. Ensure you have `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
2. Run `make setup` to create the `.venv` and install dependencies.
3. Run `make prek` to set up your prek git hooks.

## Environment variables required for local testing

```bash
export SIGMA_CLIENT_ID="your_id"
export SIGMA_CLIENT_SECRET="your_secret"
export DEPLOY_ENV="dev" # or uat, prod
```

## Useful Commands

*   `make lint` - Runs the Ruff linter.
*   `make security` - Runs Bandit security checks on the source code.
