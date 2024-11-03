from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.operation import Operation
from src.utils.constants import OperationType
from src.config.logger_config import logger

class OperationDAO:
    def __init__(
        self,
        db: Session
    ):
        self.db = db
    
    def add_operation(
        self,
        file_id: int,
        type: OperationType,
        created_by: int
    ) -> Operation:
        try:
            new_operation = Operation(
                file_id = file_id,
                type = type,
                created_by = created_by
            )
            self.db.add(new_operation)
            self.db.commit()
            self.db.refresh(new_operation)
            return new_operation

        except Exception as e:
            error_message = f'Database error occured while adding operation record to db: {e}'
            logger.error(error_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
    
    def get_operation_counts(
        self
    ):
        try:
            counts = self.db.query(
                Operation.type,
                func.count(Operation.type).label('count')
            ).group_by(Operation.type).all()

            count_dict = {operation_type: count for operation_type, count in counts}
            return count_dict
        
        except Exception as e:
            error_message = f'Database error occured while adding operation record to db: {e}'
            logger.error(error_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
