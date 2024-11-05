from pydantic import BaseModel
from typing import Optional

# User model for creating or checking user
class User(BaseModel):
    username: str
    email: str

# File model for upload
class FileUploadRequest(BaseModel):
    token: str  # JWT token to authorize user

# File response model
class FileResponse(BaseModel):
    file_id: int
    name: str
    url: str

# Operations model to fetch counts
class OperationsResponse(BaseModel):
    uploads: int
    downloads: int
    deletes: int
