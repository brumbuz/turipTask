from datetime import datetime

from pydantic import BaseModel


class Driver(BaseModel):
    id: int
    name: str
    birthday: datetime
    balance: float
    passport: str

