# CI/CD Deployment to Azure - Step-by-Step Guide

This guide walks you through deploying the containerized application to Azure using CI/CD pipelines.

## 🎯 Quick Decision: Which CI/CD Method?

| Method | Difficulty | Setup Time | Best For |
|--------|-----------|------------|----------|
| **Azure Deployment Center** | ⭐ Very Easy | 5 minutes | Quick setup, simple projects |
| **Azure DevOps Pipelines** | ⭐⭐ Medium | 15 minutes | Teams, full CI/CD |
| **GitHub Actions** | ⭐⭐ Medium | 15 minutes | GitHub-focused workflows |

**Recommendation**: Start with **Azure Deployment Center** (easiest), or use **Azure DevOps Pipelines** for full CI/CD.

---

## Method 1: Azure Deployment Center (Easiest - 5 Minutes)

### ✅ Advantages
- No pipeline configuration needed
- Automatic deployment on push to `main`
- Built into Azure Portal
- No secrets management needed

### 📋 Step-by-Step

#### Step 1: Create Azure App Services (if not done)

```bash
# Run the deployment setup script
./.azure/deploy.sh
```

Or manually:
```bash
# Create resource group
az group create --name gov-spending-rg --location eastus

# Create backend App Service
az appservice plan create --name gov-spending-api-plan --resource-group gov-spending-rg --location eastus --sku B1 --is-linux
az webapp create --resource-group gov-spending-rg --plan gov-spending-api-plan --name gov-spending-api --runtime "PYTHON|3.11"

# Create frontend App Service
az appservice plan create --name gov-spending-web-plan --resource-group gov-spending-rg --location eastus --sku B1 --is-linux
az webapp create --resource-group gov-spending-rg --plan gov-spending-web-plan --name gov-spending-web --runtime "NODE|18-lts"
```

#### Step 2: Configure Backend Deployment

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your **Backend App Service** (`gov-spending-api`)
3. Go to **"Deployment Center"** (left sidebar)
4. Select **"GitHub"** as source
5. Click **"Authorize"** and sign in to GitHub
6. Select your repository: `DevOps-Individual-Assignment-1`
7. Select branch: `main`
8. Select build provider: **"App Service build service"**
9. Configure build:
   - **Build command**: Leave default (or `pip install -r requirements.txt`)
   - **Startup command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
10. Click **"Save"**

#### Step 3: Configure Frontend Deployment

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your **Frontend App Service** (`gov-spending-web`)
3. Go to **"Deployment Center"**
4. Select **"GitHub"** as source
5. Click **"Authorize"** and sign in to GitHub
6. Select your repository: `DevOps-Individual-Assignment-1`
7. Select branch: `main`
8. Select build provider: **"App Service build service"**
9. Configure build:
   - **Build command**: `npm ci && npm run build`
   - **Output directory**: `build`
   - **Startup command**: Leave default
10. Click **"Save"**

#### Step 4: Configure Environment Variables

**Backend App Service:**
```bash
az webapp config appsettings set \
    --resource-group gov-spending-rg \
    --name gov-spending-api \
    --settings \
        DATABASE_URL="sqlite:///./government_spending.db" \
        SECRET_KEY="$(openssl rand -hex 32)" \
        CORS_ORIGINS="https://gov-spending-web.azurewebsites.net" \
        ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend App Service:**
```bash
az webapp config appsettings set \
    --resource-group gov-spending-rg \
    --name gov-spending-web \
    --settings \
        REACT_APP_API_BASE_URL="https://gov-spending-api.azurewebsites.net"
```

#### Step 5: Test Deployment

1. Make a small change to your code
2. Commit and push to `main` branch:
   ```bash
   git add .
   git commit -m "Test deployment"
   git push origin main
   ```
3. Go to Azure Portal → Your App Service → **"Deployment Center"**
4. You should see the deployment in progress
5. Wait for deployment to complete (2-5 minutes)
6. Visit your app: `https://gov-spending-api.azurewebsites.net`

**That's it!** Every push to `main` will now automatically deploy.

---

## Method 2: Azure DevOps Pipelines (Full CI/CD - 15 Minutes)

### ✅ Advantages
- Full CI/CD pipeline (tests, builds, deployment)
- Native Azure integration
- Secure service connections
- Better for teams

### 📋 Step-by-Step

#### Step 1: Create Azure DevOps Project

1. Go to [dev.azure.com](https://dev.azure.com)
2. Sign in or create account
3. Create new organization (if needed)
4. Create new project: **"Government Spending Tracker"**
5. Select **"Git"** as version control

#### Step 2: Connect GitHub Repository

1. In Azure DevOps project, go to **Project Settings** → **Repositories**
2. Click **"New Repository"** → **"GitHub"**
3. Authorize Azure DevOps to access GitHub
4. Select your repository: `DevOps-Individual-Assignment-1`
5. Click **"Create"**

#### Step 3: Create Azure Service Connection

1. Go to **Project Settings** → **Service Connections**
2. Click **"New service connection"**
3. Select **"Azure Resource Manager"**
4. Select **"Service principal (automatic)"**
5. Select your Azure subscription
6. Select resource group: `gov-spending-rg`
7. Name it: `Azure Service Connection`
8. Click **"Save"**

#### Step 4: Create Variable Group

1. Go to **Pipelines** → **Library**
2. Click **"Variable group"**
3. Name it: `gov-spending-variables`
4. Add variables:
   - `AZURE_BACKEND_APP_NAME`: `gov-spending-api`
   - `AZURE_FRONTEND_APP_NAME`: `gov-spending-web`
   - `AZURE_RESOURCE_GROUP`: `gov-spending-rg`
   - `AZURE_SERVICE_CONNECTION`: `Azure Service Connection`
5. Click **"Save"**

#### Step 5: Create Pipeline

1. Go to **Pipelines** → **Pipelines**
2. Click **"New pipeline"**
3. Select **"GitHub (YAML)"**
4. Select your repository: `DevOps-Individual-Assignment-1`
5. Select **"Existing Azure Pipelines YAML file"**
6. Select branch: `main`
7. Select path: `azure-pipelines.yml`
8. Click **"Continue"**
9. Review the pipeline
10. Click **"Run"**

#### Step 6: Link Variable Group to Pipeline

1. Go to your pipeline → **Edit**
2. Click **"Variables"** → **"Link variable group"**
3. Select `gov-spending-variables`
4. Click **"Save"**

#### Step 7: Test Pipeline

1. Make a small change to your code
2. Commit and push to `main`:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push origin main
   ```
3. Go to Azure DevOps → **Pipelines**
4. You should see the pipeline running
5. Monitor the pipeline execution
6. Once complete, your app will be deployed!

---

## Method 3: GitHub Actions (Alternative - 15 Minutes)

### ✅ Advantages
- Familiar if you use GitHub
- Good GitHub integration
- Free for public repos

### 📋 Step-by-Step

#### Step 1: Create Azure Service Principal

```bash
az ad sp create-for-rbac \
    --name "gov-spending-github-actions" \
    --role contributor \
    --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/gov-spending-rg \
    --sdk-auth
```

**Save the JSON output** - you'll need it for GitHub secrets.

#### Step 2: Get Publish Profiles

```bash
# Backend
az webapp deployment list-publishing-profiles \
    --resource-group gov-spending-rg \
    --name gov-spending-api \
    --xml

# Frontend
az webapp deployment list-publishing-profiles \
    --resource-group gov-spending-rg \
    --name gov-spending-web \
    --xml
```

**Save both XML outputs** - you'll need them for GitHub secrets.

#### Step 3: Add GitHub Secrets

1. Go to your GitHub repository
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add these secrets:
   - `AZURE_CREDENTIALS`: Paste the JSON from Step 1
   - `AZURE_BACKEND_APP_NAME`: `gov-spending-api`
   - `AZURE_FRONTEND_APP_NAME`: `gov-spending-web`
   - `AZURE_BACKEND_PUBLISH_PROFILE`: Paste XML from Step 2 (backend)
   - `AZURE_FRONTEND_PUBLISH_PROFILE`: Paste XML from Step 2 (frontend)

#### Step 4: Enable GitHub Actions Deployment

1. Go to `.github/workflows/ci.yml`
2. Uncomment the deployment jobs (remove `#` from lines 104-153)
3. Commit and push:
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "Enable Azure deployment in GitHub Actions"
   git push origin main
   ```

#### Step 5: Test Deployment

1. Make a small change
2. Commit and push to `main`
3. Go to GitHub → **Actions** tab
4. You should see the workflow running
5. Monitor the deployment
6. Once complete, your app will be deployed!

---

## 🚀 Deployment Workflow

Once CI/CD is set up, the workflow is:

1. **Developer pushes to `main` branch**
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

2. **CI/CD Pipeline Triggers**
   - Runs tests
   - Runs linting
   - Builds application
   - Deploys to Azure

3. **Automatic Deployment**
   - Backend deploys to `https://gov-spending-api.azurewebsites.net`
   - Frontend deploys to `https://gov-spending-web.azurewebsites.net`

4. **Verification**
   - Check health endpoint: `https://gov-spending-api.azurewebsites.net/health`
   - Check metrics: `https://gov-spending-api.azurewebsites.net/metrics`
   - Access frontend: `https://gov-spending-web.azurewebsites.net`

---

## 🔍 Monitoring Deployment

### Azure Portal

1. Go to Azure Portal → Your App Service
2. Go to **"Deployment Center"**
3. View deployment history
4. Check deployment logs

### Azure DevOps

1. Go to Azure DevOps → **Pipelines**
2. Select your pipeline
3. View run history
4. Click on a run to see detailed logs

### GitHub Actions

1. Go to GitHub → **Actions** tab
2. Select your workflow
3. View run history
4. Click on a run to see detailed logs

---

## 🐛 Troubleshooting

### Deployment Fails

1. **Check logs:**
   ```bash
   # Azure Portal → App Service → Log stream
   # Or
   az webapp log tail --name gov-spending-api --resource-group gov-spending-rg
   ```

2. **Check environment variables:**
   ```bash
   az webapp config appsettings list --name gov-spending-api --resource-group gov-spending-rg
   ```

3. **Check build logs:**
   - Azure Portal → Deployment Center → Logs
   - Or CI/CD pipeline logs

### App Not Working After Deployment

1. **Check health endpoint:**
   ```bash
   curl https://gov-spending-api.azurewebsites.net/health
   ```

2. **Check application logs:**
   ```bash
   az webapp log tail --name gov-spending-api --resource-group gov-spending-rg
   ```

3. **Restart App Service:**
   ```bash
   az webapp restart --name gov-spending-api --resource-group gov-spending-rg
   ```

---

## 📝 Next Steps After Deployment

1. **Update REPORT.md** with deployment results
2. **Take screenshots** of:
   - Deployment Center showing successful deployment
   - Grafana dashboard (if monitoring is set up)
   - Production URLs working
3. **Test production endpoints**
4. **Document any issues** encountered

---

## 🎯 Quick Start Checklist

- [ ] Azure App Services created
- [ ] Environment variables configured
- [ ] CI/CD method chosen (Deployment Center / DevOps / GitHub Actions)
- [ ] CI/CD configured and tested
- [ ] First deployment successful
- [ ] Health endpoints working
- [ ] Frontend accessible
- [ ] Monitoring configured (optional)

---

## 💡 Recommendation

**For fastest setup**: Use **Azure Deployment Center** (Method 1)
- Takes 5 minutes
- No pipeline configuration
- Automatic deployment on push

**For full CI/CD**: Use **Azure DevOps Pipelines** (Method 2)
- Takes 15 minutes
- Full pipeline with tests
- Better for teams

