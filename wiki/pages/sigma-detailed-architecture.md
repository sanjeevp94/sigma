---
title: "Sigma BI-as-Code Detailed Architecture"
type: "component"
sources: ["S002"]
updated: "2026-08-30"
---

# Sigma BI-as-Code Detailed Architecture

## Repository Structure (S002)

The codebase utilizes a `src/` folder for Python execution scripts and a `deploy/{env}/` folder structure (dev, uat, prod) for environment-specific configurations.

### Python Execution Scripts (S002)

- The project uses Python >=3.11, `uv` for dependency management, `ruff` for linting/formatting (line-length=120), `bandit` for security checks, and `pre-commit` for git hooks.
- Python sync scripts must be idempotent and respect the `DEPLOY_ENV` environment variable.

## CI/CD Workflow (S002)

The project uses a dual-branch CI/CD workflow:
- The `main` branch corresponds to the UAT environment.
- The `release` branch corresponds to the PROD environment.

## Infrastructure Enforcement (S002)

Redshift connections strictly enforce Graviton (rg) clusters (no RA3 allowed).

## Artifacts (S002)

Artifact JSON structures cannot be altered without downstream dbt macro verification.
