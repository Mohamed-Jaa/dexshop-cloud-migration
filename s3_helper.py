import os
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import uuid

BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "dexshop-media-storage")
REGION_NAME = os.environ.get("AWS_DEFAULT_REGION", "eu-west-3")

# AWS credentials are automatically picked up from the EC2 IAM Role
s3_client = boto3.client("s3", region_name=REGION_NAME)

def upload_product_image(file_obj, filename: str) -> str:
    """
    Uploads a product image directly to the S3 bucket under the products/ folder.
    Returns the public S3 URL of the uploaded image.
    """
    if not file_obj:
        return None

    clean_name = secure_filename(filename)
    unique_filename = f"{uuid.uuid4().hex}_{clean_name}"
    s3_key = f"products/{unique_filename}"
    
    content_type = getattr(file_obj, "content_type", "image/jpeg")

    try:
        s3_client.upload_fileobj(
            file_obj,
            BUCKET_NAME,
            s3_key,
            ExtraArgs={
                "ContentType": content_type
            }
        )
        # Construct public URL
        s3_url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{s3_key}"
        return s3_url
    except ClientError as e:
        print(f"S3 Upload Error: {e}")
        return None
