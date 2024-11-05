from typing import List
from fastapi import UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import urllib
from src.models.file import File
from src.dao.file_dao import FileDAO
from src.dao.operation_dao import OperationDAO
from src.config.logger_config import logger
from src.utils.constants import OperationType, FileStatus, DOWNLOAD_URL
from src.utils.s3_file_manager import S3FileManager

class FilesServices:
    def __init__(self, db: Session):
        self.file_dao = FileDAO(db)
        self.operation_dao = OperationDAO(db)
        self.s3_manager = S3FileManager()  # Initialize the S3 manager
    
    async def upload_file(self, file: UploadFile, user_id: int) -> File:
        try:
            object_name = file.filename
            
            # Upload the file to S3 and get the file URL
            file_url = self.s3_manager.upload_file(file, object_name)
            
            # Save file metadata in the database
            new_file = self.file_dao.add_file(
                name=object_name,
                url=file_url,
                created_by=user_id
            )

            # Log the upload operation in the database
            self.operation_dao.add_operation(
                file_id=new_file.file_id,
                type=OperationType.UPLOAD,
                created_by=user_id
            )

            logger.info(f'File with file_id: {new_file.file_id} uploaded by user with user_id: {user_id}')
            return new_file
        except Exception as e:
            logger.error(f"Error occurred while adding file record: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def delete_file(self, file_id: int, user_id: int):
        try:
            file = self.file_dao.fetch_files(file_id=file_id, status=FileStatus.ACTIVE)
            if len(file) == 0:
                error_message = f'File with ID {file_id} not found'
                logger.error(error_message)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)
            
            object_name = file[0].name
            self.s3_manager.delete_file(object_name)

            # Mark file as deleted in the database
            updated_file = self.file_dao.update_file(file_id=file_id, status=FileStatus.DELETED)
            
            # Log the delete operation in the database
            self.operation_dao.add_operation(
                file_id=updated_file.file_id,
                type=OperationType.DELETE,
                created_by=user_id
            )

            logger.info(f"File with ID {file_id} successfully deleted by user {user_id}")
            return {'response': 'Delete successful!'}
        except HTTPException as e:
            raise
        except Exception as e:
            logger.error(f"Error occurred while deleting file record with file_id: {file_id} : {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def fetch_files(self, user_id: int) -> List[File]:
        try:
            files_list = self.file_dao.fetch_files(status=FileStatus.ACTIVE)
            for file in files_list:
                file.url = DOWNLOAD_URL + str(file.file_id)
            return files_list
        except Exception as e:
            logger.error(f"Error occurred while fetching files: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def fetch_file(self, file_id: int, user_id: int):
        try:
            file_list = self.file_dao.fetch_files(file_id=file_id, status=FileStatus.ACTIVE)
            if len(file_list) == 0:
                error_message = f'File with ID {file_id} not found'
                logger.error(error_message)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)

            for file in file_list:
                self.operation_dao.add_operation(
                    file_id=file.file_id,
                    type=OperationType.DOWNLOAD,
                    created_by=user_id
                )
            object_name = file_list[0].name
            file_stream = self.s3_manager.get_file(object_name)
            
            encoded_filename = urllib.parse.quote(object_name)
            # Return the file in the response
            return StreamingResponse(file_stream, media_type="application/octet-stream", headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            })
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            logger.error(f"Error occurred while fetching file: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
