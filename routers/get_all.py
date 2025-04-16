from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime
from models.Orders import Order, Status
from progon import get_orders, get_db_connection, get_db_cursor

router = APIRouter()

@router.get("/orders", response_model=list[Order])
def read_orders(
    start_address: Optional[str] = Query(None, alias="start_address"),
    end_address: Optional[str] = Query(None, alias="end_address"),
    cost: Optional[int] = Query(None),
    order_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    car_id: Optional[int] = Query(None),
    driver_id: Optional[int] = Query(None),
    customer_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None)
):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    order_time_dt = datetime.fromisoformat(order_time) if order_time else None
    end_time_dt = datetime.fromisoformat(end_time) if end_time else None
    status_enum = Status(status) if status else None
    orders = get_orders(
        cursor,
        start_address=start_address,
        final_address=end_address,
        cost=cost,
        order_time=order_time_dt,
        end_time=end_time_dt,
        car_id=car_id,
        driver_id=driver_id,
        customer_id=customer_id,
        status=status_enum
    )
    cursor.close()
    connection.close()
    return orders