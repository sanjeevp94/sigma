---
title: "API Idempotency & Workflow Contracts"
type: "concept"
sources: ["S004"]
updated: "2026-08-30"
---

# API Idempotency & Workflow Contracts

## API Idempotency
All sync scripts (like `sync_rbac.py` and `manage_pr_workspace.py`) enforce idempotency utilizing a Read -> Diff -> Apply strategy (S004).
1. They fetch the existing state via a `GET` request.
2. They skip creation or mutating logic if the current state satisfies the configuration.
3. This guarantees that running the script twice against the same configuration results in 0 API mutations on the second run (S004).

## Client Resiliency
The `api_client.py` utilizes a custom `requests.Session` with a `urllib3.util.retry.Retry` strategy (S004). It handles `429`, `500`, `502`, `503`, and `504` errors transparently with a 3-attempt backoff mechanism.

## PR Workspace Management
Ephemeral PR workspaces (named `PR-{pr_id}`) are managed robustly:
- **Creation Collision Avoidance:** Before creating a workspace, the script searches the API. If the workspace already exists, it warns and proceeds with the existing ID rather than failing.
- **Teardown Grace:** If teardown is requested for a non-existent workspace, the script warns and exits cleanly.