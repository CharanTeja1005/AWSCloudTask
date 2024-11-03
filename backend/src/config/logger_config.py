import os
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi.logger import logger as fastapi_logger
from src.utils.constants import LoggerConfiguration

fastapi_logger.setLevel(logging.INFO)

logger_dir_relative_path = LoggerConfiguration.LOGGER_FOLDER
current_directory = os.getcwd()
logger_dir_absolute_path = os.path.join(current_directory, logger_dir_relative_path)
os.makedirs(logger_dir_absolute_path, exist_ok=True)

# Application Log Formatter
app_log_handler = TimedRotatingFileHandler(
    os.path.join(logger_dir_absolute_path, 'application_%Y-%m-%d.log'),
    backupCount=10,
    when='midnight',
    interval=1
)
app_log_handler.setLevel(logging.INFO)
app_log_handler.setFormatter(logging.Formatter(LoggerConfiguration.APP_LOG_FORMAT))

# Error Log Formatter
error_log_handler = TimedRotatingFileHandler(
    os.path.join(logger_dir_absolute_path, LoggerConfiguration.ERROR_LOGGER_FILE_FORMAT),
    backupCount=10,
    when='midnight',
    interval=1
)
error_log_handler.setLevel(logging.ERROR)
error_log_handler.setFormatter(logging.Formatter(LoggerConfiguration.ERROR_LOG_FORMAT))

fastapi_logger.addHandler(app_log_handler)
fastapi_logger.addHandler(error_log_handler)

fastapi_logger.propagate = False

logger = fastapi_logger
