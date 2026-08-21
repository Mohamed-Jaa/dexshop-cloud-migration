import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Core Application Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'insecure-dev-fallback-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///dexshop.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 12))

    # Security: Limit maximum uploaded file payload to 16MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION', 'eu-west-3')
    AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')