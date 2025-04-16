from fastapi import APIRouter, HTTPException
from models.Orders import Order
from progon import load_order, get_db_connection, get_db_cursor

router = APIRouter()

@router.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    try:
        order = load_order(cursor, order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        cursor.close()
        connection.close()
    return order