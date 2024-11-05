# src/dao/user_dao.py
from sqlalchemy.orm import Session
from src.models.user import User

class UserDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User:
        """Retrieve a user by their email."""
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, username: str, email: str) -> User:
        """Create a new user."""
        user = User(username=username, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
