from datetime import date

from pydantic import BaseModel

class Customer(BaseModel):
    id: int
    name: str
    birthday: date
    balance: float



