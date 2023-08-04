#!/bin/bash

# Check if all arguments are provided
if [ "$#" -ne 5 ]; then
  echo "Usage: $0 <project-id> <repo-name> <repo-description> <region> <image-name>"
  exit 1
fi

PROJECT_ID=$1
REPO_NAME=$2
REPO_DESCRIPTION=$3
LOCATION=$4
IMAGE_NAME=$5

gcloud artifacts repositories create "$REPO_NAME" --repository-format=docker --location="$LOCATION" --description="$REPO_DESCRIPTION"

IMAGE_URI=$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest

gcloud auth configure-docker "$LOCATION"-docker.pkg.dev

# Make sure to be in the directory that contains the Dockerfile before executing the next line
docker build ./ -t "$IMAGE_URI"

docker push "$IMAGE_URI"
