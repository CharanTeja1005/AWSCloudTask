import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException
from src.config.logger_config import logger
from src.utils.constants import S3Config

class S3FileManager:
    def __init__(self):
        """
        Initializes the S3 client with necessary credentials.
        """
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=S3Config.ACCESS_KEY,
            aws_secret_access_key=S3Config.SECRET_ACCESS_KEY,
            region_name=S3Config.REGION
        )
        self.bucket_name = S3Config.BUCKET_NAME

    def upload_file(self, file, object_name: str) -> str:
        """
        Uploads a file to S3 and returns the file URL.
        
        :param file: File to upload.
        :param object_name: Name of the object in S3.
        :return: URL of the uploaded file.
        """
        try:
            self.s3_client.upload_fileobj(file.file, self.bucket_name, object_name)
            file_url = f"https://{self.bucket_name}.s3.{S3Config.REGION}.amazonaws.com/{object_name}"
            logger.info(f"File uploaded to S3 at {file_url}.")
            return file_url
        except NoCredentialsError:
            logger.error("AWS credentials not found.")
            raise
        except ClientError as e:
            logger.error(f"An error occurred while uploading to S3: {e}")
            raise

    def delete_file(self, object_name: str) -> bool:
        """
        Deletes a file from S3.

        :param object_name: Name of the object to delete.
        :return: True if file was deleted, else False.
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            logger.info(f"File {object_name} deleted from S3.")
            return True
        except ClientError as e:
            logger.error(f"An error occurred while deleting from S3: {e}")
            return False

    def get_file(self, object_name: str):
        """
        Retrieves a file from S3.

        :param object_name: Name of the object in S3.
        :return: File stream from S3.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_name)
            return response['Body']  # Returns the file stream
        except ClientError as e:
            logger.error(f"An error occurred while retrieving the file from S3: {e}")
            raise HTTPException(status_code=500, detail="Could not retrieve the file.")