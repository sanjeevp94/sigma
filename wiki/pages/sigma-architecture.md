---
title: "Sigma BI-as-Code Architecture"
type: "concept"
sources: ["S001"]
updated: "2026-08-30"
---

# Sigma BI-as-Code Architecture

The repository manages the Business Intelligence environment using a strictly version-controlled, GitOps-managed infrastructure utilizing the Sigma v2 REST API (S001).

## Core Concepts (S001)

- **Bitbucket is the source of truth.** Manual UI changes will be overwritten.
- **RBAC and Workspaces** are declarative and defined in `deploy/`.
- **Infrastructure (Redshift)** enforces Graviton instance types.

## Development Setup (S001)

We use `uv` for ultra-fast python environments.

1. Ensure you have `uv` installed.
2. Run `make setup` to create the `.venv` and install dependencies.
3. Run `make prek` to set up your prek git hooks.

Environment variables required for local testing:
- `SIGMA_CLIENT_ID`
- `SIGMA_CLIENT_SECRET`
- `DEPLOY_ENV` (dev, uat, prod)
