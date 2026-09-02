import os
import uuid
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def is_allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_storage(file_storage_object) -> str:
    """
    يرفع الصورة مباشرة إلى AWS S3 عبر الـ IAM Role (أو مفاتيح AWS CLI محلياً).
    في حال الفشل أو عدم التوفر، يحفظها احتياطياً داخل static/uploads/.
    """
    if not file_storage_object or file_storage_object.filename == '':
        return None

    if not is_allowed_file(file_storage_object.filename):
        raise ValueError("Unsupported file extension. Allowed formats: png, jpg, jpeg, webp.")

    clean_name = secure_filename(file_storage_object.filename)
    extension = clean_name.rsplit('.', 1)[1].lower() if '.' in clean_name else 'jpg'
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    s3_key = f"products/{unique_filename}"

    bucket_name = os.environ.get("S3_BUCKET_NAME", "dexshop-media-storage")
    region_name = os.environ.get("AWS_DEFAULT_REGION", "eu-west-3")

    content_type = getattr(file_storage_object, "content_type", "image/jpeg")

    try:
        s3_client = boto3.client("s3", region_name=region_name)
        s3_client.upload_fileobj(
            file_storage_object,
            bucket_name,
            s3_key,
            ExtraArgs={"ContentType": content_type}
        )
        return f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{s3_key}"
    except ClientError as e:
        if current_app:
            current_app.logger.error(f"S3 Upload failed: {e}")
        # حفظ محلي احتياطي
        local_dir = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(local_dir, exist_ok=True)
        file_path = os.path.join(local_dir, unique_filename)
        file_storage_object.seek(0)
        file_storage_object.save(file_path)
        return f"/static/uploads/{unique_filename}"