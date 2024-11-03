from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.sql import func
from src.config.database_config import base
from src.models.user import User
from src.models.file import File
from src.utils.constants import TableName, OperationType

class Operation(base):
    __tablename__ = TableName.OPERATION

    operation_id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey(File.file_id), nullable=False)
    type = Column(Enum(OperationType))
    created_by = Column(Integer, ForeignKey(User.user_id), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
