from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.dao.user_dao import UserDAO
from src.utils.jwt import create_jwt_token
from src.config.database_initializer import get_db

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str

@router.post("/users")
def check_or_create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_dao = UserDAO(db)
    existing_user = user_dao.get_user_by_email(user.email)

    if existing_user:
        # User exists, create and return JWT token
        token = create_jwt_token(existing_user.user_id, existing_user.username, existing_user.email)
        return {"message": "User already exists", "token": token}

    # User does not exist, create a new user
    new_user = user_dao.create_user(username=user.username, email=user.email)
    token = create_jwt_token(new_user.user_id, new_user.username, new_user.email)
    
    return {"message": "User created successfully", "token": token}
