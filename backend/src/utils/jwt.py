import jwt
from fastapi import HTTPException, status
from src.utils.constants import SECRET_KEY

def create_jwt_token(user_id: int, username: str, email: str) -> str:
    payload = {
        "sub": user_id,  # User ID as the subject
        "username": username,
        "email": email,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")  # Extract user ID from the payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
