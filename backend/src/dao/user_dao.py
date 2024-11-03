# src/dao/user_dao.py
from sqlalchemy.orm import Session
from src.models.user import User

class UserDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_auth0_id(self, auth0_id: str) -> User:
        return self.db.query(User).filter(User.auth0_id == auth0_id).first()

    def create_user(self, auth0_id: str, username: str = None, email: str = None) -> User:
        user = User(auth0_id=auth0_id, username=username, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, username: str = None, email: str = None) -> User:
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.username = username or user.username
            user.email = email or user.email
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
