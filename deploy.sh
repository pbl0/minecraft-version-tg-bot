#!/bin/bash

# Minecraft Version Change Telegram Bot Deployment Script
# Builds and publishes to registry only (no container run)

set -e

REGISTRY="192.168.1.119:5000"
PROJECT_NAME="minecraft-version-tg-bot"

echo "🚀 Starting build and registry push for $PROJECT_NAME..."

# Build image locally
echo "🔨 Building image locally..."
podman build -t localhost/$PROJECT_NAME .

# Tag for registry
echo "🏷️  Tagging for registry..."
podman tag localhost/$PROJECT_NAME $REGISTRY/$PROJECT_NAME

# Push to registry
echo "📤 Pushing image to registry..."
podman push --tls-verify=false $REGISTRY/$PROJECT_NAME

echo "✅ Build and registry push completed successfully!"
echo "🐳 Image available at: $REGISTRY/$PROJECT_NAME"