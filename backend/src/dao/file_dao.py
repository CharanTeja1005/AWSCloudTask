from typing import List
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from sqlalchemy.exc import NoResultFound
from src.models.file import File
from src.utils.constants import FileStatus
from src.config.logger_config import logger

class FileDAO:
    def __init__(
        self,
        db: Session
    ):
        self.db = db
    
    def add_file(
        self,
        name: str,
        url: str,
        created_by: int
    ) -> File:
        try:
            new_file = File(
                name = name,
                url = url,
                created_by = created_by,
                status = FileStatus.ACTIVE
            )
            self.db.add(new_file)
            self.db.commit()
            self.db.refresh(new_file)
            return new_file
        except Exception as e:
            error_message = f'Database error occured while adding file record to db: {e}'
            logger.error(error_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
    
    def update_file(
        self,
        file_id: int,
        **fields
    ) -> File:
        try:
            file = self.db.query(File).filter(file_id == File.file_id).one()

            for attribute, value in fields.items():
                if hasattr(file, attribute):
                    setattr(file, attribute, value)
            
            self.db.commit()
            return file
        
        except NoResultFound as e:
            error_message = f'File with {file_id} not found: {e}'
            logger.error(error_message)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)
        except Exception as e:
            error_message = f'Database error occured while updating file record with file_id {file_id} to db: {e}'
            logger.error(error_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
    
    def fetch_files(
        self,
        **filters
    ) -> List[File]:
        try:
            files = self.db.query(File)

            for attribute, value in filters.items():
                if hasattr(File, attribute):
                    files = files.filter(getattr(File, attribute) == value)
            
            return files.all()
        except Exception as e:
            error_message = f'Database error occured while fetching files: {e}'
            logger.error(error_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)