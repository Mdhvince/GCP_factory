# ML on GCP

## Vertex AI training

![alt text](docs/training_job.png "Vertex AI training job")

***
**Upload the data to the bucket**
```bash
# upload a file
./upload_to_bucket.sh --type file /path/to/local/file.txt my-bucket-name
# upload a folder
./upload_to_bucket.sh --type folder /path/to/local/folder my-bucket-name
```

**Setup the container**
```bash
./setup_container_training_service.sh <your-project-id> <repo-name> <your-repo-description> <your-region> <your-image-name>
```
Note: <repo-name> does not support underscore, use dash instead.

**Run the training job**
```bash
python run_training_job.py --project_id <project_id> \
                           --bucket_name <bucket_name> \
                           --region <region> \
                           --repo_name <repo_name> \
                           --image_name <image_name> \
                           --machine_type <machine_type> \
                           --list_training_args <arg1=val1 arg2=val2 arg3=val3> \
                           #...
```

during training, it is optional but recommended to save the model in **torchscript** format. Torchscript is a way to
create serializable and optimized Pytorch models for inference. This can be done as follows:
```python
import torch

model = ...
# train the model and save the state dict as usual
# at the end, convert the best model to torchscript

torch_scripted_model = torch.jit.script(model)
torch_scripted_model.save("ts_model.pt")
```


## Vertex AI prediction with torchserve

`pip install torchserve torch-model-archiver torch-workflow-archiver`

- Use **torchserve handler** to initialize/preprocess/inference/postprocess data.
- Create the Dockerfile with torchserve as base image and package everything.
- Build the image and push it to the artifact registry.



