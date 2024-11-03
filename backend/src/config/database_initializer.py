from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from src.config.database_config import base, engine, session_local
from src.models import *


models = [File, Operation, User]

base.metadata.create_all(bind=engine, tables=[model.__table__ for model in models])

def get_db() -> Generator[Session, None, None]:
    db = session_local()
    try:
        yield db
    finally:
        db.close()
