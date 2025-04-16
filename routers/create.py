from fastapi import APIRouter
from models.Orders import Order, OrderCreate
from progon import save_order, get_db_connection, get_db_cursor

router = APIRouter()

@router.post("/orders", response_model=Order)
def create_order(order: OrderCreate):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    saved_order = save_order(cursor, order)
    cursor.close()
    connection.close()
    return saved_order
