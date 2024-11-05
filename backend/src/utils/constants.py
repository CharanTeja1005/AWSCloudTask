import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class TableName:
    USER: str = 'user'
    FILE: str = 'file'
    OPERATION: str = 'operation'

class FileStatus(str, Enum):
    ACTIVE: str = 'active'
    DELETED: str = 'deleted'

class OperationType(str, Enum):
    UPLOAD: str = 'upload'
    DOWNLOAD: str = 'download'
    DELETE: str = 'delete'

class LoggerConfiguration:
    LOGGER_FOLDER: str = 'src/logs'
    LOGGER_FILE: str = 'src/logs/application.logs'
    APP_LOGGER_FILE_FORMAT = 'application_%Y-%m-%d.log'
    APP_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    ERROR_LOGGER_FILE_FORMAT = 'error_%Y-%m-%d.log'
    ERROR_LOG_FORMAT = '%(asctime)s - ERROR - %(message)s'

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB = os.getenv('MYSQL_DB')
DATABASE_URL = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'

class S3Config:
    BUCKET_NAME=os.getenv('BUCKET_NAME')
    ACCESS_KEY=os.getenv('ACCESS_KEY')
    SECRET_ACCESS_KEY=os.getenv('SECRET_ACCESS_KEY')
    REGION=os.getenv('REGION')

DOWNLOAD_URL = 'http://localhost:8000/files/'

SECRET_KEY = os.getenv('SECRET_KEY')