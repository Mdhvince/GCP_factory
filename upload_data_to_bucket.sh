#!/bin/bash

# Check if the number of arguments is less than 3
if [[ $# -lt 3 ]]; then
  echo "Usage: $0 --type <file|folder> <LOCAL_FILE_PATH|FOLDER_PATH> <BUCKET_NAME>"
  exit 1
fi

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --type)
      shift
      type=$1
      ;;
    *)
      break
      ;;
  esac
  shift
done

if [[ "$type" != "file" && "$type" != "folder" ]]; then
  echo "Invalid type. Use --type <file|folder>"
  exit 1
fi

# Get the file or folder path and bucket name
file_or_folder_path=$1
bucket_name=$2

# Perform the appropriate action based on the type
if [[ "$type" == "file" ]]; then
  gsutil cp "$file_or_folder_path" "gs://$bucket_name"
elif [[ "$type" == "folder" ]]; then
  gsutil -m cp -r "$file_or_folder_path" "gs://$bucket_name"
fi
