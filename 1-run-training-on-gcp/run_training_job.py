import argparse
from datetime import datetime

from google.cloud import aiplatform


def parser_fn():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project_id", type=str, help="GCP project ID",
    )
    parser.add_argument(
        "--bucket_name", type=str, help="Name of the bucket without the gs:// prefix. Only the bucket name.",
    )
    parser.add_argument(
        "--region", type=str, help="Region to run the training job (e.g., us-central1)",
    )
    parser.add_argument(
        "--repo_name", type=str, help="Name of the repo (docker artifact registry, no underscores allowed)",
    )
    parser.add_argument(
        "--image_name", type=str, help="Name of the image (docker artifact registry, e.g. my_image:latest)",
    )
    parser.add_argument(
        "--machine_type", type=str, help="Machine type to run the training job (e.g., n1-standard-4)",
    )

    parser.add_argument(
        "--list_training_args", type=str, nargs="+",
        help="""List of training arguments e.g.
                --list_training_args \
                train_dir=/gcs/my-bucket/data \
                model_path=/gcs/my-bucket/model""",
    )
    parser.add_argument(
        "--accelerator_type", type=str, help="Type of accelerator to use (e.g., NVIDIA_TESLA_T4)",
        default="ACCELERATOR_TYPE_UNSPECIFIED",
    )
    parser.add_argument(
        "--accelerator_count", type=int, help="Number of accelerators to use", default=0,
    )
    parser.add_argument(
        "--replica_count", type=int, help="Number of replicas to run the training job.", default=1,
    )
    parser.add_argument(
        "--tensorboard_display_name", type=str,
        help="Name of the Tensorboard instance", default="tensorboard-" + datetime.now().strftime("%Y%m%d%H%M%S"),
    )
    parser.add_argument(
        "--job_name", type=str,
        help="Name of the training job", default="training-" + datetime.now().strftime("%Y%m%d%H%M%S"),
    )

    args = parser.parse_args()
    return args



if __name__ == "__main__":
    args = parser_fn()

    if args.accelerator_type == "ACCELERATOR_TYPE_UNSPECIFIED":
        args.accelerator_count = 0

    if args.accelerator_type != "ACCELERATOR_TYPE_UNSPECIFIED":
        assert args.accelerator_count > 0

    aiplatform.init(location=args.region)
    tensorboard = aiplatform.Tensorboard.create(display_name=args.tensorboard_display_name)

    IMAGE_URI = f"{args.region}-docker.pkg.dev/{args.project_id}/{args.repo_name}/{args.image_name}"

    my_job = aiplatform.CustomContainerTrainingJob(
        display_name=args.job_name,
        container_uri=IMAGE_URI,
        staging_bucket=f"gs://{args.bucket_name}",
    )

    training_args = ["--" + arg for arg in args.list_training_args]

    my_job.run(
        args=training_args,
        replica_count=args.replica_count,
        machine_type=args.machine_type,
        accelerator_type=args.accelerator_type,
        accelerator_count=args.accelerator_count,
        tensorboard=tensorboard.resource_name,
    )


