from typing import List
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, Security
from sqlalchemy.orm import Session
from src.config.database_initializer import get_db
from src.services.files_services import FilesServices
from src.utils.jwt import decode_jwt_token
from src.config.logger_config import logger

router = APIRouter()

# Dependency to extract user ID from JWT token
def get_current_user(token: str) -> int:
    return decode_jwt_token(token)  # Decode and return the user ID

@router.post('/files')
async def files_router_post(
    file: UploadFile,
    db: Session = Depends(get_db),
    token: str = Security(get_current_user)  # Expect the token as input
):
    user_id = token
    logger.info(f"User ID {user_id} is attempting to upload file: {file.filename}")
    
    try:
        return await FilesServices(db).upload_file(file, user_id)  # Pass user ID directly
    except Exception as e:
        logger.error(f"Error occurred while uploading file record: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/files')
async def files_router_get(
    db: Session = Depends(get_db),
    token: str = Security(get_current_user)  # Expect the token as input
):
    user_id = token
    try:
        return await FilesServices(db).fetch_files(user_id)  # Pass user ID directly
    except Exception as e:
        logger.error(f"Error occurred while fetching file records: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/files/{file_id}')
async def files_router_get_file(
    file_id: int,
    db: Session = Depends(get_db),
    token: str = Security(get_current_user)  # Expect the token as input
):
    user_id = token
    print(token)
    try:
        return await FilesServices(db).fetch_file(file_id=file_id, user_id=user_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error occurred while fetching file record with file_id: {file_id} : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete('/files/{file_id}')
async def files_router_delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    token: str = Security(get_current_user)  # Expect the token as input
):
    user_id = token
    try:
        return await FilesServices(db).delete_file(file_id=file_id, user_id=user_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error occurred while deleting file record with file_id: {file_id} : {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
