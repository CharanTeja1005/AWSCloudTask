from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database_initializer import get_db
from src.dao.operation_dao import OperationDAO
from src.config.logger_config import logger

router = APIRouter()

@router.get('/operations')
async def operations_route_get(
    db: Session = Depends(get_db)
) -> dict:
    try:
        return OperationDAO(db).get_operation_counts()
    except Exception as e:
        logger.error(f"Error occurred while getting operation counts: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
