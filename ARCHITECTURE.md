# Proxymity BI-as-Code: Sigma Solution Design

## 1. Migration Strategy & Architecture Principle
This repository transitions our Business Intelligence environment from a manual, UI-driven platform to a strictly version-controlled, GitOps-managed infrastructure utilizing the Sigma v2 REST API.

**The Gatekeeper Principle:**
Bitbucket is the ultimate source of truth. Any manual UI changes to managed assets (workbooks, data models, workspaces, connections) will be systematically overwritten during the next Jenkins CI/CD pipeline run. To enforce this, the Jenkins Service Account is the **only** identity granted `Admin` or `Editor` roles on production workspaces.

---

## 2. SSO Management & License Allocation (AWS IAM Identity Center)
To maintain our Bitbucket repository as the source of truth for Role-Based Access Control (RBAC) while automating user onboarding, we utilize **SAML Just-In-Time (JIT) Provisioning combined with our GitOps API pipeline**, bypassing strict SCIM to avoid API read-only lockouts.

### JIT Provisioning & SAML Assertions
When a user logs in via AWS SSO for the first time, Sigma automatically creates their account and assigns their base license role.
* **Role Enforcement:** We pass the `userRole` attribute from AWS to Sigma during SAML authentication. If a user attempts to escalate privileges in the Sigma UI, their next SSO login will revert them to their AWS-defined license state.
* **Team Allocation (The GitOps Handoff):** AWS handles authentication and license assignment. Our `teams.yaml` and Jenkins pipeline handle the actual Sigma Team allocation and workspace permissions.

### Licensing Strategy
* **Creator (Admin) [1 License]:** Dedicated strictly to the Jenkins Service Account for API operations.
* **Creator [N Licenses]:** Assigned via AWS to the core data engineering and data science teams building JSON models in designated development workspaces.
* **Explorer/Viewer:** Assigned via AWS to all business stakeholders based on their requirement to explore vs. consume data.

---

## 3. Repository Structure & Antigravity Setup
The repository strictly separates declarative state (`deploy/`), artifacts (`artifacts/`), and the execution engine (`src/`).

```text
sigma-bi-as-code/
├── ARCHITECTURE.md            # This document
├── Jenkinsfile                # CI/CD Orchestration
├── pyproject.toml             # uv dependency declaration
├── Makefile                   # Helper commands
├── .pre-commit-config.yaml    # Pre-commit hooks for linting/security
├── AGENTS.md                  # Autonomous agent instructions (Jules/Antigravity)
├── deploy/
│   ├── dev/                   # Dev environment configurations
│   ├── uat/                   # UAT environment configurations
│   └── prod/                  # PROD environment configurations
│       ├── teams.yaml             # RBAC mappings
│       ├── connections.yaml       # Database targets (Redshift)
│       ├── workspaces.yaml        # Folder hierarchies and permissions
│       └── tags.yaml              # Version tagging logic
├── artifacts/
│   ├── data_models/
│   │   └── dummy_model.json
│   └── workbooks/
│       └── executive_summary.json
└── src/                       # Execution Engine
    ├── sync_rbac.py
    ├── sync_connections.py
    ├── sync_artifacts.py
    ├── sync_tags.py
    └── utils/
        └── api_client.py
```

### Agent Directives (AGENTS.md)
Antigravity and Jules use this file to govern how AI agents interact with this repository during pull requests. Ensures idempotency, environment awareness (`DEPLOY_ENV`), and strict infrastructure rules.

---

## 4. Configuration State (The Source of Truth)
The `deploy/` directory defines the exact state of the environment, separated into subdirectories per deployment environment (`dev`, `uat`, `prod`).

### deploy/prod/teams.yaml (Example)
Maps users to specific groups for RBAC.
```yaml
teams:
  - name: Data Engineering
    members:
      - k.simakov@proxymity.io
  - name: Data Science
    members:
      - s.ahmad@proxymity.io
```

### deploy/prod/connections.yaml (Example)
Target data warehouses. Passwords are never stored here; they are injected securely by Jenkins. Ensure Redshift clusters use Graviton (rg).
```yaml
connections:
  - name: redshift-prod
    type: redshift
    properties:
      host: prod-cluster-rg.cxxxxxxxxxx.eu-west-1.redshift.amazonaws.com
      port: 5439
      database: analytics_prod
      user: sigma_svc_prod
```

### deploy/prod/workspaces.yaml (Example)
Folder hierarchies locked down by code.
```yaml
workspaces:
  - name: Core Reporting
    description: Production analytics
    permissions:
      - team: Data Engineering
        role: editor
      - team: Data Science
        role: viewer
```

---

## 5. Tag Syncing & UAT/PROD Release Strategy
We utilize a **Dual-Branch Workflow** (main and release) combined with Sigma Version Tags to manage UAT testing and zero-downtime PROD deployments on a single asset.

### The Mechanics:
 1. **UAT Deployment (main branch):** When code merges to main, Jenkins pushes the new JSON to Sigma. The workbook ID remains the same, but the internal version increments. Jenkins updates the UAT tag to point to this new version.
 2. **PROD Release (release branch):** Once UAT is approved, a PR is opened from main to release. When merged, Jenkins **does not** push JSON again. It simply updates the PROD tag to point to the approved version.

---

## 6. Execution Engine (Python + uv)
We use `uv` for ultra-fast, reproducible dependency management inside Jenkins. Scripts in `src/` are environment aware, utilizing `DEPLOY_ENV` to determine which folder in `deploy/` to read.

---

## 7. CI/CD Orchestration (Jenkinsfile)
The declarative pipeline pulls secured credentials, resolves dependencies via `uv`, and injects the `DEPLOY_ENV` variable into the execution context based on the active branch.
