import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from utils.constants import S3Config

# Replace these values with your own
AWS_ACCESS_KEY = S3Config.ACCESS_KEY
AWS_SECRET_KEY = S3Config.SECRET_ACCESS_KEY
REGION_NAME = 'us-east-1'  # Change to your region
BUCKET_NAME = S3Config.BUCKET_NAME
TEST_FILE_NAME = 'test_file.txt'
TEST_FILE_CONTENT = 'This is a test file for S3 upload.'

def upload_file_to_s3(file_name: str, bucket: str, object_name: str = None):
    # Initialize S3 client
    print(AWS_ACCESS_KEY)
    print(AWS_SECRET_KEY)
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME
    )
    
    if object_name is None:
        object_name = file_name  # Use the file name as the object name if not specified
    
    try:
        # Create a test file
        with open(file_name, 'w') as file:
            file.write(TEST_FILE_CONTENT)
        
        # Upload the file
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File '{file_name}' uploaded to bucket '{bucket}' as '{object_name}'")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except NoCredentialsError:
        print("AWS credentials not found.")
    except ClientError as e:
        print(f"An error occurred: {e}")

# Call the upload function
upload_file_to_s3(TEST_FILE_NAME, BUCKET_NAME)
