from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    pending = "pending"
    processing = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class Order(BaseModel):
    id: int
    start_address: str
    final_address: str
    cost: float
    order_time: datetime
    end_time: datetime
    car_id: int
    drivers_id: int
    customer_id: int
    status: Status

