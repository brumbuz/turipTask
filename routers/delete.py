from fastapi import APIRouter, HTTPException
from models.Orders import Order
from progon import delete_order, get_db_connection, get_db_cursor

router = APIRouter()

@router.delete("/orders/{order_id}", response_model=Order)
def delete_order_endpoint(order_id: int):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    try:
        order = delete_order(cursor, order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        cursor.close()
        connection.close()
    return order