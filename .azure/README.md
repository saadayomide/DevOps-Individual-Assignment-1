# Azure Deployment Guide

This guide explains how to deploy the Government Spending Tracker application to Azure App Service.

## Prerequisites

1. **Azure Account**: Sign up at [azure.microsoft.com](https://azure.microsoft.com)
2. **Azure CLI**: Install from [docs.microsoft.com/cli/azure](https://docs.microsoft.com/cli/azure/install-azure-cli)
3. **GitHub Repository**: Your code should be in a GitHub repository (for CI/CD)

## Quick Start

### Option 1: Automated Setup Script (Recommended)

**Step 1: Create `.env` file (optional but recommended)**

```bash
# Copy the example file
cp .azure/.env.example .azure/.env

# Edit .azure/.env with your values
# The .env file is gitignored and won't be committed
```

**Step 2: Run the deployment setup script**

```bash
# Run the deployment setup script
./.azure/deploy.sh
```

This script will:
- Load configuration from `.azure/.env` if it exists
- Create resource group
- Create App Service plans
- Create backend and frontend App Services
- Configure environment variables from `.env` file
- Generate publish profiles

**Note**: The `.env` file is gitignored and will not be committed to version control.

### Option 2: Manual Setup

#### 1. Login to Azure

```bash
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

#### 2. Create Resource Group

```bash
az group create --name gov-spending-rg --location eastus
```

#### 3. Create Backend App Service

```bash
# Create App Service Plan
az appservice plan create \
    --name gov-spending-api-plan \
    --resource-group gov-spending-rg \
    --location eastus \
    --sku B1 \
    --is-linux

# Create Web App
az webapp create \
    --resource-group gov-spending-rg \
    --plan gov-spending-api-plan \
    --name gov-spending-api \
    --runtime "PYTHON|3.11"
```

#### 4. Configure Backend Environment Variables

```bash
az webapp config appsettings set \
    --resource-group gov-spending-rg \
    --name gov-spending-api \
    --settings \
        DATABASE_URL="sqlite:///./government_spending.db" \
        SECRET_KEY="$(openssl rand -hex 32)" \
        CORS_ORIGINS="https://gov-spending-web.azurewebsites.net" \
        ACCESS_TOKEN_EXPIRE_MINUTES=30 \
        WEBSITES_ENABLE_APP_SERVICE_STORAGE=false \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

#### 5. Create Frontend App Service

```bash
# Create App Service Plan
az appservice plan create \
    --name gov-spending-web-plan \
    --resource-group gov-spending-rg \
    --location eastus \
    --sku B1 \
    --is-linux

# Create Web App
az webapp create \
    --resource-group gov-spending-rg \
    --plan gov-spending-web-plan \
    --name gov-spending-web \
    --runtime "NODE|18-lts"
```

#### 6. Configure Frontend Environment Variables

```bash
az webapp config appsettings set \
    --resource-group gov-spending-rg \
    --name gov-spending-web \
    --settings \
        REACT_APP_API_BASE_URL="https://gov-spending-api.azurewebsites.net" \
        WEBSITES_ENABLE_APP_SERVICE_STORAGE=false \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

## Deployment Methods

### Method 1: Azure CLI (Quick Deploy)

**Backend:**
```bash
cd backend
az webapp up \
    --name gov-spending-api \
    --resource-group gov-spending-rg \
    --runtime "PYTHON|3.11"
```

**Frontend:**
```bash
cd frontend
npm run build
az webapp up \
    --name gov-spending-web \
    --resource-group gov-spending-rg \
    --runtime "NODE|18-lts"
```

### Method 2: Azure DevOps Pipelines (CI/CD) - Recommended for Azure

**✅ Recommended if you're using Azure**: Use Azure's native CI/CD platform.

**Advantages:**
- Native Azure integration
- No external service needed
- Can use Azure Service Connections (more secure than GitHub secrets)
- Full CI/CD pipeline with testing, building, and deployment

**Setup:**

1. **Create Azure DevOps Project:**
   - Go to [dev.azure.com](https://dev.azure.com)
   - Create a new project
   - Connect your GitHub repository

2. **Create Service Connection:**
   - Go to Project Settings → Service Connections
   - Create new Azure Resource Manager connection
   - Name it: `Azure Service Connection`
   - Select your subscription and resource group

3. **Configure Pipeline Variables:**
   - Go to Pipelines → Library → Variable Groups
   - Create variable group: `gov-spending-variables`
   - Add variables:
     - `AZURE_BACKEND_APP_NAME`: `gov-spending-api`
     - `AZURE_FRONTEND_APP_NAME`: `gov-spending-web`
     - `AZURE_RESOURCE_GROUP`: `gov-spending-rg`

4. **Create Pipeline:**
   - Go to Pipelines → New Pipeline
   - Select your repository (GitHub)
   - Choose "Existing Azure Pipelines YAML file"
   - Select `azure-pipelines.yml`
   - Run the pipeline

**Pipeline File:** `azure-pipelines.yml` is included in the repository.

### Method 3: GitHub Actions (CI/CD) - Optional

**⚠️ Important**: This is OPTIONAL. You can use Azure DevOps Pipelines instead.

**Note**: GitHub Secrets are ONLY needed if you want to use GitHub Actions. For Azure deployments, Azure DevOps Pipelines is recommended.

1. **Create Azure Service Principal:**
```bash
az ad sp create-for-rbac \
    --name "gov-spending-github-actions" \
    --role contributor \
    --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/gov-spending-rg \
    --sdk-auth
```

2. **Add GitHub Secrets:**
   - Go to your GitHub repository → Settings → Secrets → Actions
   - Add the following secrets:
     - `AZURE_CREDENTIALS`: Output from the service principal command above (JSON format)
     - `AZURE_BACKEND_APP_NAME`: `gov-spending-api`
     - `AZURE_FRONTEND_APP_NAME`: `gov-spending-web`
     - `AZURE_BACKEND_PUBLISH_PROFILE`: Get from Azure Portal or CLI (XML format)
     - `AZURE_FRONTEND_PUBLISH_PROFILE`: Get from Azure Portal or CLI (XML format)

3. **Get Publish Profiles:**
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

**Alternative**: You can also use your local `.env` file values as a reference when setting up GitHub secrets.

### Method 4: Azure App Service Deployment Center (Simplest)

**✅ Easiest method**: Connect GitHub directly to Azure App Service.

**Advantages:**
- No pipeline configuration needed
- Automatic deployment on push to main branch
- Built into Azure Portal
- Simple setup (5 minutes)

**Setup:**

1. **Backend Deployment:**
   - Go to Azure Portal → Your Backend App Service
   - Go to "Deployment Center"
   - Select source: "GitHub"
   - Authorize Azure to access your GitHub account
   - Select repository and branch (main)
   - Select build provider: "App Service build service"
   - Save

2. **Frontend Deployment:**
   - Go to Azure Portal → Your Frontend App Service
   - Go to "Deployment Center"
   - Select source: "GitHub"
   - Authorize Azure to access your GitHub account
   - Select repository and branch (main)
   - Select build provider: "App Service build service"
   - Set build command: `npm run build`
   - Set output directory: `build`
   - Save

**That's it!** Every push to `main` branch will automatically deploy.

### Method 5: Azure Portal Manual Deployment

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your App Service
3. Go to "Advanced Tools" → "Go" (Kudu)
4. Use the file manager or drag-and-drop to upload files
5. Or use FTP/FTPS to upload files

## Environment Variables

### Using Local `.env` File

The easiest way to manage environment variables is using a local `.env` file:

1. **Copy the example file:**
   ```bash
   cp .azure/.env.example .azure/.env
   ```

2. **Edit `.azure/.env` with your values:**
   - Fill in your Azure subscription ID
   - Set your app names
   - Configure backend and frontend settings
   - Generate a secret key: `openssl rand -hex 32`

3. **The `.env` file is gitignored** - it won't be committed to version control

4. **The deployment script automatically reads from `.env`** when you run `./.azure/deploy.sh`

### Backend App Service

| Variable | Description | Example | In .env |
|----------|-------------|---------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./government_spending.db` | ✅ |
| `SECRET_KEY` | JWT secret key | Generate with `openssl rand -hex 32` | ✅ |
| `CORS_ORIGINS` | Allowed CORS origins | `https://gov-spending-web.azurewebsites.net` | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` | ✅ |

### Frontend App Service

| Variable | Description | Example | In .env |
|----------|-------------|---------|---------|
| `REACT_APP_API_BASE_URL` | Backend API URL | `https://gov-spending-api.azurewebsites.net` | ✅ |

## Monitoring

### Health Check

- Backend: `https://gov-spending-api.azurewebsites.net/health`
- Frontend: `https://gov-spending-web.azurewebsites.net/health`

### Metrics

- Backend: `https://gov-spending-api.azurewebsites.net/metrics`

### Application Insights (Optional)

```bash
# Create Application Insights
az monitor app-insights component create \
    --app gov-spending-insights \
    --location eastus \
    --resource-group gov-spending-rg

# Get instrumentation key
az monitor app-insights component show \
    --app gov-spending-insights \
    --resource-group gov-spending-rg \
    --query instrumentationKey
```

## Troubleshooting

### View Logs

```bash
# Backend logs
az webapp log tail --name gov-spending-api --resource-group gov-spending-rg

# Frontend logs
az webapp log tail --name gov-spending-web --resource-group gov-spending-rg
```

### Check Deployment Status

```bash
az webapp deployment list \
    --resource-group gov-spending-rg \
    --name gov-spending-api
```

### Restart App Service

```bash
az webapp restart --name gov-spending-api --resource-group gov-spending-rg
```

## Cost Optimization

- Use **F1 (Free)** tier for development/testing
- Use **B1 (Basic)** tier for production (low traffic)
- Use **S1 (Standard)** tier for production (higher traffic)
- Enable auto-shutdown for development environments

## Security Best Practices

1. **Never commit secrets** - Use `.env` file (gitignored) or Azure App Service Configuration
2. **Enable HTTPS** - Azure App Service provides free SSL certificates
3. **Use Managed Identity** - For accessing other Azure resources
4. **Enable Application Insights** - For monitoring and security alerts
5. **Regular updates** - Keep dependencies updated

## Next Steps

- Set up custom domain
- Configure SSL certificates
- Set up Application Insights
- Configure auto-scaling
- Set up staging slots

## Deployment Methods Comparison

| Method | Difficulty | Automation | Best For |
|--------|-----------|------------|----------|
| **Local Deployment** (`.env` file) | ⭐ Easy | Manual | Development, testing |
| **Azure DevOps Pipelines** | ⭐⭐ Medium | Full CI/CD | Teams, production |
| **Azure Deployment Center** | ⭐ Very Easy | Automatic | Quick setup, simple projects |
| **GitHub Actions** | ⭐⭐ Medium | Full CI/CD | GitHub-focused workflows |

## Local vs CI/CD Deployment

### Local Deployment (Using .env File) - NO Secrets Needed

- **Use case**: Deploying from your local machine using Azure CLI
- **Configuration**: Create `.azure/.env` file from `.azure/.env.example`
- **GitHub Secrets**: ❌ **NOT REQUIRED** - You don't need GitHub secrets for local deployment
- **Advantages**: 
  - Easy to manage secrets locally
  - No need to set up GitHub secrets
  - Fast iteration during development
  - Full control over deployment process
- **How to deploy:**
  ```bash
  # 1. Create .env file
  cp .azure/.env.example .azure/.env
  # Edit .azure/.env with your values
  
  # 2. Run deployment script
  ./.azure/deploy.sh
  
  # 3. Deploy manually
  cd backend
  az webapp up --name gov-spending-api --resource-group gov-spending-rg
  ```

### CI/CD Deployment Options

#### Option A: Azure DevOps Pipelines (Recommended for Azure)

- **Use case**: Full CI/CD with Azure's native platform
- **Configuration**: Azure Service Connections (more secure than secrets)
- **Secrets**: ✅ Uses Azure Service Connections (no GitHub secrets needed)
- **Advantages**:
  - Native Azure integration
  - Secure service connections
  - Full pipeline with tests, builds, deployment
  - Can use Azure Key Vault for secrets
- **Setup**: See Method 2 above

#### Option B: Azure Deployment Center (Simplest)

- **Use case**: Quick automatic deployment from GitHub
- **Configuration**: Connect GitHub repo in Azure Portal
- **Secrets**: ❌ Not needed - Azure handles authentication
- **Advantages**:
  - Easiest setup (5 minutes)
  - No pipeline configuration
  - Automatic deployment on push
  - Built into Azure Portal
- **Setup**: See Method 4 above

#### Option C: GitHub Actions (Alternative)

- **Use case**: Using GitHub's CI/CD platform
- **Configuration**: Add secrets to GitHub repository
- **GitHub Secrets**: ✅ Required - GitHub Actions runs on GitHub's servers
- **Advantages**:
  - Familiar if you use GitHub
  - Good GitHub integration
  - Free for public repos
- **Setup**: See Method 3 above

### Choose Your Deployment Method

**Option 1: Local Deployment Only (Recommended for Development)**
- ✅ Use `.env` file
- ❌ No secrets needed
- ✅ Simple and straightforward
- ✅ Good for development and testing

**Option 2: Azure Deployment Center (Recommended for Simplicity)**
- ✅ Connect GitHub repo in Azure Portal
- ❌ No secrets needed
- ✅ Automatic deployment
- ✅ Easiest CI/CD setup

**Option 3: Azure DevOps Pipelines (Recommended for Teams/Production)**
- ✅ Use Azure Service Connections
- ✅ Full CI/CD pipeline
- ✅ Secure and scalable
- ✅ Best for production

**Option 4: GitHub Actions (Alternative)**
- ✅ Use GitHub secrets
- ✅ Good GitHub integration
- ✅ Free for public repos

