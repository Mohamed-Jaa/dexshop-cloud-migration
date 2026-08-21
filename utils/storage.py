import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
import boto3
from botocore.exceptions import ClientError

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def is_allowed_file(filename):
    """
    Validates file extension against a secure whitelist.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_storage(file_storage_object):
    """
    Handles file upload securely:
    - Generates a collision-resistant UUID filename.
    - Uploads to AWS S3 if credentials exist.
    - Gracefully falls back to local static/uploads/ directory in local development.
    Returns: The accessible URL/path of the uploaded file.
    """
    if not file_storage_object or file_storage_object.filename == '':
        return None

    if not is_allowed_file(file_storage_object.filename):
        raise ValueError("Unsupported file extension. Allowed formats: png, jpg, jpeg, webp.")

    # Generate a cryptographically secure random filename
    original_name = secure_filename(file_storage_object.filename)
    extension = original_name.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{extension}"

    bucket_name = current_app.config.get('AWS_S3_BUCKET_NAME')
    access_key = current_app.config.get('AWS_ACCESS_KEY_ID')
    secret_key = current_app.config.get('AWS_SECRET_ACCESS_KEY')
    region = current_app.config.get('AWS_REGION', 'eu-west-3')

    # Path 1: Production AWS S3 Upload
    if bucket_name and access_key and secret_key:
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            s3_client.upload_fileobj(
                file_storage_object,
                bucket_name,
                unique_filename,
                ExtraArgs={'ContentType': file_storage_object.content_type}
            )
            return f"https://{bucket_name}.s3.{region}.amazonaws.com/{unique_filename}"
        except ClientError as error:
            current_app.logger.error(f"S3 Upload failed: {error}")
            raise RuntimeError("Cloud storage upload error.")

    # Path 2: Local Development Storage Fallback
    local_upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(local_upload_dir, exist_ok=True)

    file_path = os.path.join(local_upload_dir, unique_filename)
    file_storage_object.save(file_path)

    return f"/static/uploads/{unique_filename}"