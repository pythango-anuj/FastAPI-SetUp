from fastapi import Depends
from app.config.database import get_db


class DBService:
    def __init__(self, db = Depends(get_db)) -> None:
        self.db = db
        

class BaseCRUD(DBService):
    pass


class BaseService(DBService):
    pass
