from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class TagSchema(BaseModel):
    uid: UUID
    name: str
    created_at: datetime

class TagCreateModel(BaseModel):
    name: str = Field(min_length=2, max_length=50)

class TagResponse(BaseModel):
    message: str
    tag: TagSchema
