from beanie import PydanticObjectId
from fastapi_users import schemas
from typing import Optional


class UserRead(schemas.BaseUser[PydanticObjectId]):
    name: Optional[str]


class UserCreate(schemas.BaseUserCreate):
    name: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str] = None