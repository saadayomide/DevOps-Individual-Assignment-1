#!/bin/bash
# Azure deployment script
# This script helps set up and deploy the application to Azure App Service
# It reads configuration from .azure/.env file if it exists

set -e

echo "🚀 Azure Deployment Script for Government Spending Tracker"
echo "============================================================"

# Load environment variables from .env file if it exists
ENV_FILE=".azure/.env"
if [ -f "$ENV_FILE" ]; then
    echo "📄 Loading configuration from $ENV_FILE"
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "⚠️  No .env file found. Using defaults or prompting for values."
    echo "   Create .azure/.env from .azure/.env.example for easier configuration."
fi

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if logged in
if ! az account show &> /dev/null; then
    echo "🔐 Please log in to Azure:"
    az login
fi

# Get subscription and resource group from env or prompt
if [ -z "$AZURE_SUBSCRIPTION_ID" ]; then
    read -p "Enter Azure subscription ID (or press Enter to use default): " SUBSCRIPTION_ID
    if [ -n "$SUBSCRIPTION_ID" ]; then
        AZURE_SUBSCRIPTION_ID="$SUBSCRIPTION_ID"
    fi
fi

if [ -n "$AZURE_SUBSCRIPTION_ID" ]; then
    az account set --subscription "$AZURE_SUBSCRIPTION_ID"
fi

RESOURCE_GROUP=${AZURE_RESOURCE_GROUP:-gov-spending-rg}
LOCATION=${AZURE_LOCATION:-eastus}
BACKEND_APP_NAME=${AZURE_BACKEND_APP_NAME:-gov-spending-api}
FRONTEND_APP_NAME=${AZURE_FRONTEND_APP_NAME:-gov-spending-web}

# Prompt for values if not in .env
if [ -z "$AZURE_RESOURCE_GROUP" ]; then
    read -p "Enter resource group name (default: $RESOURCE_GROUP): " INPUT_RESOURCE_GROUP
    RESOURCE_GROUP=${INPUT_RESOURCE_GROUP:-$RESOURCE_GROUP}
fi

if [ -z "$AZURE_LOCATION" ]; then
    read -p "Enter location (default: $LOCATION): " INPUT_LOCATION
    LOCATION=${INPUT_LOCATION:-$LOCATION}
fi

if [ -z "$AZURE_BACKEND_APP_NAME" ]; then
    read -p "Enter backend app name (default: $BACKEND_APP_NAME): " INPUT_BACKEND_APP_NAME
    BACKEND_APP_NAME=${INPUT_BACKEND_APP_NAME:-$BACKEND_APP_NAME}
fi

if [ -z "$AZURE_FRONTEND_APP_NAME" ]; then
    read -p "Enter frontend app name (default: $FRONTEND_APP_NAME): " INPUT_FRONTEND_APP_NAME
    FRONTEND_APP_NAME=${INPUT_FRONTEND_APP_NAME:-$FRONTEND_APP_NAME}
fi

echo ""
echo "📋 Configuration:"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   Location: $LOCATION"
echo "   Backend App: $BACKEND_APP_NAME"
echo "   Frontend App: $FRONTEND_APP_NAME"
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Create resource group
echo "📦 Creating resource group..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" || true

# Create backend App Service
echo "🔧 Creating backend App Service..."
az webapp create \
    --resource-group "$RESOURCE_GROUP" \
    --plan "${BACKEND_APP_NAME}-plan" \
    --name "$BACKEND_APP_NAME" \
    --runtime "PYTHON|3.11" \
    || az appservice plan create \
        --name "${BACKEND_APP_NAME}-plan" \
        --resource-group "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --sku B1 \
        --is-linux \
    && az webapp create \
        --resource-group "$RESOURCE_GROUP" \
        --plan "${BACKEND_APP_NAME}-plan" \
        --name "$BACKEND_APP_NAME" \
        --runtime "PYTHON|3.11"

# Configure backend
echo "⚙️  Configuring backend..."
BACKEND_SECRET_KEY=${SECRET_KEY:-$(openssl rand -hex 32)}
BACKEND_DATABASE_URL=${DATABASE_URL:-sqlite:///./government_spending.db}
BACKEND_CORS_ORIGINS=${CORS_ORIGINS:-https://${FRONTEND_APP_NAME}.azurewebsites.net}
BACKEND_TOKEN_EXPIRE=${ACCESS_TOKEN_EXPIRE_MINUTES:-30}

az webapp config appsettings set \
    --resource-group "$RESOURCE_GROUP" \
    --name "$BACKEND_APP_NAME" \
    --settings \
        WEBSITES_ENABLE_APP_SERVICE_STORAGE=false \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true \
        DATABASE_URL="$BACKEND_DATABASE_URL" \
        SECRET_KEY="$BACKEND_SECRET_KEY" \
        CORS_ORIGINS="$BACKEND_CORS_ORIGINS" \
        ACCESS_TOKEN_EXPIRE_MINUTES="$BACKEND_TOKEN_EXPIRE"

# Create frontend App Service
echo "🔧 Creating frontend App Service..."
az webapp create \
    --resource-group "$RESOURCE_GROUP" \
    --plan "${FRONTEND_APP_NAME}-plan" \
    --name "$FRONTEND_APP_NAME" \
    --runtime "NODE|18-lts" \
    || az appservice plan create \
        --name "${FRONTEND_APP_NAME}-plan" \
        --resource-group "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --sku B1 \
        --is-linux \
    && az webapp create \
        --resource-group "$RESOURCE_GROUP" \
        --plan "${FRONTEND_APP_NAME}-plan" \
        --name "$FRONTEND_APP_NAME" \
        --runtime "NODE|18-lts"

# Configure frontend
FRONTEND_API_URL=${REACT_APP_API_BASE_URL:-https://${BACKEND_APP_NAME}.azurewebsites.net}
echo "⚙️  Configuring frontend..."
az webapp config appsettings set \
    --resource-group "$RESOURCE_GROUP" \
    --name "$FRONTEND_APP_NAME" \
    --settings \
        REACT_APP_API_BASE_URL="$FRONTEND_API_URL" \
        WEBSITES_ENABLE_APP_SERVICE_STORAGE=false \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true

# Get publish profiles
echo "📥 Getting publish profiles..."
az webapp deployment list-publishing-profiles \
    --resource-group "$RESOURCE_GROUP" \
    --name "$BACKEND_APP_NAME" \
    --xml > backend-publish-profile.xml

az webapp deployment list-publishing-profiles \
    --resource-group "$RESOURCE_GROUP" \
    --name "$FRONTEND_APP_NAME" \
    --xml > frontend-publish-profile.xml

echo ""
echo "✅ Deployment setup complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 LOCAL DEPLOYMENT (Using .env file) - NO GitHub Secrets Needed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   1. Your .env file is already configured with these values!"
echo ""
echo "   2. Deploy backend:"
echo "      cd backend"
echo "      az webapp up --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP"
echo ""
echo "   3. Deploy frontend:"
echo "      cd frontend"
echo "      npm run build"
echo "      az webapp up --name $FRONTEND_APP_NAME --resource-group $RESOURCE_GROUP"
echo ""
echo "   ✅ That's it! No GitHub secrets needed for local deployment."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 CI/CD DEPLOYMENT (GitHub Actions) - GitHub Secrets Required"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   ⚠️  Only needed if you want automatic deployment via GitHub Actions"
echo "   ⚠️  GitHub Actions runs on GitHub's servers and cannot access your local .env file"
echo ""
echo "   1. Add secrets to GitHub repository (Settings → Secrets → Actions):"
echo "      - AZURE_CREDENTIALS (Service Principal credentials)"
echo "      - AZURE_BACKEND_APP_NAME: $BACKEND_APP_NAME"
echo "      - AZURE_FRONTEND_APP_NAME: $FRONTEND_APP_NAME"
echo "      - AZURE_BACKEND_PUBLISH_PROFILE (from backend-publish-profile.xml)"
echo "      - AZURE_FRONTEND_PUBLISH_PROFILE (from frontend-publish-profile.xml)"
echo ""
echo "   2. Push to main branch to trigger automatic deployment"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 URLs:"
echo "   Backend:  https://${BACKEND_APP_NAME}.azurewebsites.net"
echo "   Frontend: https://${FRONTEND_APP_NAME}.azurewebsites.net"
echo ""
echo "💡 Tip: For local deployment, you ONLY need the .env file - no GitHub secrets!"

