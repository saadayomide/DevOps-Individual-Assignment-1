# Azure DevOps Pipelines Setup Guide

This guide explains how to set up CI/CD using Azure DevOps Pipelines for the Government Spending Tracker application.

## Prerequisites

1. **Azure Account**: Sign up at [azure.microsoft.com](https://azure.microsoft.com)
2. **Azure DevOps Account**: Sign up at [dev.azure.com](https://dev.azure.com) (free)
3. **GitHub Repository**: Your code should be in a GitHub repository

## Quick Setup (5 Steps)

### Step 1: Create Azure DevOps Project

1. Go to [dev.azure.com](https://dev.azure.com)
2. Create a new organization (if you don't have one)
3. Create a new project: "Government Spending Tracker"
4. Select "Git" as version control (we'll connect GitHub later)

### Step 2: Connect GitHub Repository

1. Go to Project Settings → Repositories
2. Click "New Repository" → "GitHub"
3. Authorize Azure DevOps to access your GitHub account
4. Select your repository: `DevOps-Individual-Assignment-1`
5. Click "Create"

### Step 3: Create Azure Service Connection

1. Go to Project Settings → Service Connections
2. Click "New service connection"
3. Select "Azure Resource Manager"
4. Select "Service principal (automatic)"
5. Select your Azure subscription
6. Select your resource group: `gov-spending-rg`
7. Name it: `Azure Service Connection`
8. Click "Save"

### Step 4: Create Variable Group

1. Go to Pipelines → Library
2. Click "Variable group"
3. Name it: `gov-spending-variables`
4. Add variables:
   - `AZURE_BACKEND_APP_NAME`: `gov-spending-api`
   - `AZURE_FRONTEND_APP_NAME`: `gov-spending-web`
   - `AZURE_RESOURCE_GROUP`: `gov-spending-rg`
5. Click "Save"

### Step 5: Create Pipeline

1. Go to Pipelines → Pipelines
2. Click "New pipeline"
3. Select "GitHub" (YAML)
4. Select your repository: `DevOps-Individual-Assignment-1`
5. Select "Existing Azure Pipelines YAML file"
6. Select branch: `main`
7. Select path: `azure-pipelines.yml`
8. Click "Continue"
9. Review the pipeline
10. Click "Run"

## Pipeline Overview

The pipeline consists of 3 stages:

### Stage 1: Test
- **Backend Tests**: Runs ruff, mypy, bandit, and pytest with coverage
- **Frontend Tests**: Runs npm test with coverage
- **Coverage Report**: Publishes coverage results

### Stage 2: Build
- **Docker Images**: Builds backend and frontend Docker images
- **Optional**: Can push to Azure Container Registry

### Stage 3: Deploy
- **Backend Deployment**: Deploys to Azure App Service
- **Frontend Deployment**: Builds and deploys to Azure App Service

## Pipeline Variables

The pipeline uses the following variables (configure in Variable Group):

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_BACKEND_APP_NAME` | Backend App Service name | `gov-spending-api` |
| `AZURE_FRONTEND_APP_NAME` | Frontend App Service name | `gov-spending-web` |
| `AZURE_RESOURCE_GROUP` | Azure resource group | `gov-spending-rg` |
| `AZURE_SERVICE_CONNECTION` | Azure Service Connection name | `Azure Service Connection` |

## Environment Configuration

### Backend Environment Variables

Configure in Azure Portal → App Service → Configuration → Application settings:

- `DATABASE_URL`: `sqlite:///./government_spending.db`
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `CORS_ORIGINS`: `https://gov-spending-web.azurewebsites.net`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`

### Frontend Environment Variables

Configure in Azure Portal → App Service → Configuration → Application settings:

- `REACT_APP_API_BASE_URL`: `https://gov-spending-api.azurewebsites.net`

## Pipeline Triggers

The pipeline triggers on:
- Push to `main` branch
- Pull requests to `main` branch (runs tests only)

## Manual Deployment

You can also trigger the pipeline manually:

1. Go to Pipelines → Pipelines
2. Select your pipeline
3. Click "Run pipeline"
4. Select branch: `main`
5. Click "Run"

## Troubleshooting

### Pipeline Fails on Tests

- Check test coverage (must be ≥70%)
- Fix linting errors (ruff, mypy, bandit)
- Check test logs for details

### Pipeline Fails on Deployment

- Verify Azure Service Connection is configured correctly
- Check App Service names match variable group
- Verify resource group exists
- Check App Service is running

### Pipeline Fails on Build

- Check Dockerfiles are correct
- Verify dependencies are installed
- Check build logs for errors

## Advantages of Azure DevOps Pipelines

✅ **Native Azure Integration**: Seamless integration with Azure services
✅ **Secure**: Uses Azure Service Connections (more secure than secrets)
✅ **Free**: Free for public repositories and limited private repos
✅ **Full CI/CD**: Complete pipeline with tests, builds, and deployment
✅ **Scalable**: Can handle complex deployment scenarios
✅ **Monitoring**: Built-in pipeline monitoring and logging

## Next Steps

- Set up pipeline approvals for production deployments
- Configure staging environments
- Set up release pipelines
- Configure pipeline notifications
- Set up pipeline analytics

