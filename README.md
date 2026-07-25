# Sigma BI-as-Code

This repository manages the Business Intelligence environment using a strictly version-controlled, GitOps-managed infrastructure utilizing the Sigma v2 REST API.

## Core Concepts

*   **Bitbucket is the source of truth.** Manual UI changes will be overwritten.
*   **RBAC and Workspaces** are declarative and defined in `deploy/`.
*   **Infrastructure (Redshift)** enforces Graviton instance types.

## Development Setup

We use `uv` for ultra-fast python environments.

1. Ensure you have `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
2. Run `make setup` to create the `.venv` and install dependencies.
3. Run `make pre-commit` to set up your pre-commit git hooks.

## Environment variables required for local testing

```bash
export SIGMA_CLIENT_ID="your_id"
export SIGMA_CLIENT_SECRET="your_secret"
export DEPLOY_ENV="dev" # or uat, prod
```

## Useful Commands

*   `make lint` - Runs the Ruff linter.
*   `make security` - Runs Bandit security checks on the source code.
