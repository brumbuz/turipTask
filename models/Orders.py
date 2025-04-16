from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    canceled = "canceled"

class Order(BaseModel):
    id: int
    start_address: str
    final_address: str
    cost: int
    order_time: datetime
    end_time: datetime
    car_id: int
    driver_id: int
    customer_id: int
    status: Status

class OrderCreate(BaseModel):
    start_address: str
    final_address: str
    cost: int
    order_time: datetime
    end_time: datetime
    car_id: int
    driver_id: int
    customer_id: int
    status: Status

class OrderUpdate(BaseModel):
    start_address: Optional[str] = None
    final_address: Optional[str] = None
    cost: Optional[int] = None
    order_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    car_id: Optional[int] = None
    driver_id: Optional[int] = None
    customer_id: Optional[int] = None
    status: Optional[Status] = None