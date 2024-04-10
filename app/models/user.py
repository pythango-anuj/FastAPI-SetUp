from typing import List, Optional
from beanie import Document
from fastapi_users.db import BaseOAuthAccount, BeanieBaseUser, BeanieUserDatabase
from pydantic import Field
from app.models.base import TimestampMixin


class OAuthAccount(BaseOAuthAccount):
    pass


class User(BeanieBaseUser, TimestampMixin, Document):
    name: Optional[str] = None
    oauth_accounts: List[OAuthAccount] = Field(default_factory=list)


async def get_user_db():
    yield BeanieUserDatabase(User, OAuthAccount)
