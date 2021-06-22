from datetime import datetime
from pydantic import BaseModel


class roles_request(BaseModel):
    name: str
    url: str
    method: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode=True
