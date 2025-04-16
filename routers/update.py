from fastapi import APIRouter, HTTPException
from models.Orders import OrderUpdate
from progon import update_order, load_order, get_db_connection, get_db_cursor

router = APIRouter()

@router.put("/orders/{order_id}")
def update_order_endpoint(order_id: int, order_update: OrderUpdate):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    try:
        load_order(cursor, order_id)  # Проверка существования заказа
        update_order(cursor, order_id, order_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        cursor.close()
        connection.close()
    return {"message": "Заказ обновлен"}

