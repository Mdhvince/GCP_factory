# Google cloud helpers
***
- `classifier-training` : Directory containing the code for containerizing the training of the classifier.
- `classifier-training/Dockerfile` : Dockerfile for the containerization of the training of the classifier.
- `classifier-training/trainer` : Package containing the code for the training of the classifier.

Once the Dockerfile is filled, I follow the instruction from [My personal cheatsheet](https://www.notion.so/medhy-vinceslas/GCP-d5f7cea5a9aa459ca4221af6a334c3bd) to build
the container and push it to the Google Artifact Registry and run the training job on Vertex AI.  
  
***
Upload the data to the bucket
```bash
# upload a file
./upload_to_bucket.sh --type file /path/to/local/file.txt my-bucket-name
# upload a folder
./upload_to_bucket.sh --type folder /path/to/local/folder my-bucket-name
```

