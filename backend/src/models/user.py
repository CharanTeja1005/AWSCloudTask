# src/models/user.py
from sqlalchemy import Column, Integer, String
from src.config.database_config import base
from src.utils.constants import TableName

class User(base):
    __tablename__ = TableName.USER

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
