#!/bin/bash

# I assume the repository is already created (it contains the training image)
# Check if all arguments are provided
if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <project-id> <repo-name> <region> <predict-image-name>"
  exit 1
fi

PROJECT_ID=$1
REPO_NAME=$2
LOCATION=$3
PREDICT_IMAGE_NAME=$4

# Build the image
CUSTOM_PREDICTOR_IMAGE_URI=$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/predict-$PREDICT_IMAGE_NAME:latest
docker build ./ -t "$CUSTOM_PREDICTOR_IMAGE_URI"

# Wait for the user to press enter to push the image now
read -p "Press enter to push the image to the artifact registry"

# Push the image to the artifact registry
docker push "$CUSTOM_PREDICTOR_IMAGE_URI"
