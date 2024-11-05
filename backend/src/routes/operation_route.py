from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from src.config.database_initializer import get_db
from src.dao.operation_dao import OperationDAO
from src.config.logger_config import logger
from src.utils.jwt import decode_jwt_token  # Import the JWT decoding utility

router = APIRouter()

# Dependency to extract user ID from JWT token
def get_current_user(token: str) -> dict:
    user_id = decode_jwt_token(token)
    return {'user_id': user_id}

@router.get('/operations')
async def operations_route_get(
    db: Session = Depends(get_db),
    token: str = Security(get_current_user)  # Use the Security dependency to extract token
) -> dict:
    try:
        return OperationDAO(db).get_operation_counts()
    except Exception as e:
        logger.error(f"Error occurred while getting operation counts: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
