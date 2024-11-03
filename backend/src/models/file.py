from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.sql import func
from src.config.database_config import base
from src.models.user import User
from src.utils.constants import TableName, FileStatus

class File(base):
    __tablename__ = TableName.FILE

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey(User.user_id), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    status = Column(Enum(FileStatus))
