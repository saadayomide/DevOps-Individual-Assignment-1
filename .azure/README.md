# Azure Deployment (GitHub Actions First)

This repository now relies entirely on **GitHub Actions** for continuous integration and deployment to Azure App Service. This document explains how to provision credentials, wire up secrets, and troubleshoot the workflow.

## 1. Prerequisites

- Azure subscription with:
  - Resource Group (e.g. `BCSAI2025-DEVOPS-STUDENTS-A`)
  - Azure Container Registry (ACR) (e.g. `govspendingacr2`)
  - Two Linux App Services (backend + frontend) already created and pointed at your ACR repositories
- Azure CLI installed locally (`az login`).
- GitHub repository access (to add secrets and monitor workflow runs).

## 2. Create a Service Principal for GitHub Actions

```bash
az ad sp create-for-rbac \
  --name "gov-spending-github-actions" \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP> \
  --sdk-auth
```

Copy the JSON output and store it as the GitHub secret `AZURE_CREDENTIALS`.

## 3. Gather ACR Credentials

```bash
az acr credential show --name <ACR_NAME>
```

Record:
- `username` → `AZURE_ACR_USERNAME`
- `passwords[0].value` (or regenerate via `az acr credential renew --password-name password`) → `AZURE_ACR_PASSWORD`
- `loginServer` (e.g. `govspendingacr2.azurecr.io`) → `AZURE_ACR_LOGIN_SERVER`

## 4. Required GitHub Secrets / Variables

Add the following under **Repository → Settings → Secrets and variables → Actions**:

| Name | Purpose |
|------|---------|
| `AZURE_CREDENTIALS` | Service principal JSON from step 2 |
| `AZURE_RESOURCE_GROUP` | Resource group that hosts the App Services + ACR |
| `AZURE_BACKEND_APP_NAME` | Backend App Service name (e.g. `gov-spending-api`) |
| `AZURE_FRONTEND_APP_NAME` | Frontend App Service name (e.g. `gov-spending-web`) |
| `AZURE_ACR_LOGIN_SERVER` | e.g. `govspendingacr2.azurecr.io` |
| `AZURE_ACR_USERNAME` | ACR admin username |
| `AZURE_ACR_PASSWORD` | ACR admin password |
| `BACKEND_IMAGE_NAME` | Container repo path inside ACR (e.g. `gov-spending/backend`) |
| `FRONTEND_IMAGE_NAME` | Container repo path inside ACR (e.g. `gov-spending/frontend`) |

Non-sensitive values can be stored as “repository variables”, but keeping everything as secrets also works.

## 5. What the Workflow Does

Workflow: `.github/workflows/ci-cd.yml`

1. Runs backend (Python) and frontend (Node) tests on every push/PR.
2. On pushes to `main`, logs into ACR, builds both Docker images, tags them (`latest` + commit SHA), and pushes.
3. Uses `azure/login` + `az webapp config container set` to point the App Services at the new image tags and restarts them.

No `.env` files or legacy scripts are required—deployment is fully automated once the secrets are set.

## 6. Optional Alternatives

- **Azure Deployment Center:** For a quick demo, you can connect GitHub → App Service via the portal. Azure will build/deploy automatically, bypassing the workflow.
- **Manual CLI:** You can still run `az webapp config container set` or `az webapp restart` locally for emergency fixes, but these are not part of the standard process anymore.

## 7. App Service Configuration Checklist

Make sure each App Service has the proper settings (Portal → Configuration → Application settings):

| Setting | Backend | Frontend |
|---------|---------|----------|
| `DATABASE_URL` | ✅ | – |
| `SECRET_KEY` | ✅ | – |
| `CORS_ORIGINS` | ✅ | – |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ✅ | – |
| `WEBSITES_PORT` | `8000` | `80` |
| `WEBSITE_HEALTHCHECK_PATH` | `/health` | `/health` (optional) |
| `WEBSITE_HEALTHCHECK_MAXPINGFAILURES` | `2` | `2` |
| `REACT_APP_API_BASE_URL` | – | `https://<backend>.azurewebsites.net` |

## 8. Troubleshooting Tips

- **ImagePullFailure**: Usually means the ACR credentials are wrong/missing. Regenerate passwords via `az acr credential show` and update the GitHub secrets.  
- **App Service shows “Application Error”**: Use `az webapp log tail --name <app> --resource-group <rg>` or Portal → Log Stream to inspect container logs.  
- **Workflow fails at `azure/login`**: Ensure `AZURE_CREDENTIALS` JSON has not expired and that the service principal still has Contributor rights on the resource group.

With these pieces in place, pushing to `main` is enough to run tests, build new containers, and redeploy both Azure App Services automatically.

