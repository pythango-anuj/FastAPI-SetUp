from pydantic import BaseModel, root_validator
from datetime import datetime


class TimestampMixin(BaseModel):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    class Config:
        validate_assignment = True

    @root_validator(pre=True)
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values
    

class BaseModelMixin(TimestampMixin):
    pass
