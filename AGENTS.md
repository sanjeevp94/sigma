# Sigma BI-as-Code Engineering Standards

This file governs how AI agents interact with this repository during pull requests.

1. **Idempotency:** Python sync scripts inside `src/` must query the existing Sigma state before executing POST/PUT requests. Ensure states are compared appropriately to avoid unnecessary updates.
2. **Infrastructure:** Never configure Redshift connections using RA3 instance types; strictly enforce Graviton (rg) clusters.
3. **Artifacts:** Do not alter workbook JSON structures inside `artifacts/workbooks/` without verifying downstream dbt macro compatibility.
4. **Environment Isolation:** The source of truth for deployments lives in `deploy/{env}` where `{env}` is dev, uat, or prod. Make sure sync scripts respect the `DEPLOY_ENV` environment variable to pick up configuration from the correct directory.
5. **GitOps Strictness:** Jenkins is the only authorized editor of production environments. Do not propose architectures that rely on UI modifications or side-channel access.
