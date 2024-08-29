from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, field_validator, Field, EmailStr, HttpUrl


class StatusType(str, Enum):
    DONE = 'done'
    PENDING = 'pending'


class Category(BaseModel):
    id: int = Field(gt=0)
    name: str

    class Config:
        from_attributes = True


class Tag(BaseModel):
    id: int = Field(gt=0)
    name: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str = Field(min_length=3)
    surname: str
    email: EmailStr
    website: HttpUrl

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int = Field(gt=0)


class AccessToken(BaseModel):
    user_id: int
    access_token: str
    expiration_date: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    name: str
    description: str = Field('No description', min_length=5)
    status: StatusType
    category_id: int = Field(gt=0)

    class Config:
        from_attributes = True

    @field_validator('name')
    def id_name_alphanumeric(cls, v: str):
        assert v.replace(' ', '').isalnum(), 'Name must be alphanumeric'
        return v


class TaskRead(TaskBase):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)

    created_at: datetime
    updated_at: datetime


class TaskReadComplete(TaskBase):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)

    user: UserRead
    category: Category
    tags: List[Tag]

    created_at: datetime
    updated_at: datetime | None


class TaskWrite(TaskBase):
    user_id: Optional[int] = Field()
