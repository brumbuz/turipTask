from pydantic import BaseModel

class Car(BaseModel):
    id: int
    numbers: str
    stamp: str

