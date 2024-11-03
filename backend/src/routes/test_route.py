from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dao.operation_dao import OperationDAO
from src.config.database_initializer import get_db

test_router = APIRouter()

@test_router.post('/test')
async def test(
        request: dict,
        db: Session = Depends(get_db)
    ):
    return OperationDAO(db).get_operation_counts()
