#!/bin/bash
set -e

VERSION=${1:-latest}
IMAGE_NAME="aditya040305/drift-guard-agent"

echo "Building Docker image ${IMAGE_NAME}:${VERSION}..."
docker build -t "${IMAGE_NAME}:${VERSION}" .

echo "Tagging as latest..."
docker tag "${IMAGE_NAME}:${VERSION}" "${IMAGE_NAME}:latest"

echo "Pushing ${IMAGE_NAME}:${VERSION} to Docker Hub..."
docker push "${IMAGE_NAME}:${VERSION}"

echo "Pushing ${IMAGE_NAME}:latest to Docker Hub..."
docker push "${IMAGE_NAME}:latest"

echo "Done!"
