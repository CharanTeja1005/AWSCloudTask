from typing import List
from fastapi import APIRouter, Depends, File as UploadFileDependency, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database_initializer import get_db
from src.services.files_services import FilesServices
from src.models.file import File
from src.dao.file_dao import FileDAO
from src.dao.operation_dao import OperationDAO
from src.config.logger_config import logger
from src.utils.constants import OperationType

router = APIRouter()

@router.post('/files')
async def files_router_post(
    file: UploadFile = UploadFileDependency(...),
    db: Session = Depends(get_db),
    current_user: dict = {'user_id': 1}
):
    logger.info(f"User {current_user['user_id']} is attempting to upload file: {file.filename}")
    
    try:
        return await FilesServices(db).upload_file(file, current_user)
    except Exception as e:
        logger.error(f"Error occurred while uploading file record: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/files')
async def files_router_get(
    db: Session = Depends(get_db)
):
    try:
        return await FilesServices(db).fetch_files()
    except Exception as e:
        logger.error(f"Error occurred while fetching file records: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/files/{file_id}')
async def files_router_get_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    try:
        return await FilesServices(db).fetch_file(file_id=file_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error occurred while fetching file record with file_id: {file_id} : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete('/files/{file_id}')
async def files_router_delete_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    try:
        return await FilesServices(db).delete_file(file_id = file_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error occurred while fetching file record with file_id: {file_id} : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
