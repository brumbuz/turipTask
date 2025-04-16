import os
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv
import psycopg2 as pc
from models.Cars import Car
from models.Customers import Customer
from models.Drivers import Driver
from models.Orders import Order, Status, OrderCreate, OrderUpdate

load_dotenv()


def get_db_connection():
    return pc.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def get_db_cursor(connection):
    return connection.cursor()


def save_car(cursor, stamp: str, number: str):
    cursor.execute(
        "INSERT INTO vasilev_goncharov.Cars (number, stamp) VALUES (%s, %s)",
        (number, stamp))
    cursor.connection.commit()


def load_car(cursor, car_id: int) -> Car:
    cursor.execute("SELECT * FROM vasilev_goncharov.Cars WHERE id = %s", (car_id,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"Машина с id {car_id} не найдена")
    return Car(id=row[0], number=row[1], stamp=row[2])


def save_driver(cursor, name: str, birthday: datetime, balance: int, passport: Optional[str] = None):
    cursor.execute(
        "INSERT INTO vasilev_goncharov.Drivers (name, birthday, balance, passport) VALUES (%s, %s, %s, %s)",
        (name, birthday, balance, passport)
    )
    cursor.connection.commit()


def load_driver(cursor, driver_id: int) -> Driver:
    cursor.execute("SELECT * FROM vasilev_goncharov.Drivers WHERE id = %s", (driver_id,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"Водитель с id {driver_id} не найден")
    return Driver(id=row[0], name=row[1], birthday=row[2], balance=row[3], passport=row[4])


def save_customer(cursor, name: str, birthday: datetime, balance: int):
    cursor.execute(
        "INSERT INTO vasilev_goncharov.Customers (name, birthday, balance) VALUES (%s, %s, %s)",
        (name, birthday, balance)
    )
    cursor.connection.commit()


def load_customer(cursor, customer_id: int) -> Customer:
    cursor.execute("SELECT * FROM vasilev_goncharov.Customers WHERE id = %s", (customer_id,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"Клиент с id {customer_id} не найден")
    return Customer(id=row[0], name=row[1], birthday=row[2], balance=row[3])


def save_order(cursor, order: OrderCreate) -> Order:
    cursor.execute(
        """INSERT INTO vasilev_goncharov.Orders 
        (start_address, final_address, cost, order_time, end_time, car_id, driver_id, customer_id, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
        (order.start_address, order.final_address, order.cost, order.order_time, order.end_time,
         order.car_id, order.driver_id, order.customer_id, order.status.value)
    )
    order_id = cursor.fetchone()[0]
    cursor.connection.commit()
    return load_order(cursor, order_id)


def load_order(cursor, order_id: int) -> Order:
    cursor.execute("SELECT * FROM vasilev_goncharov.Orders WHERE id = %s", (order_id,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"Заказ с id {order_id} не найден")
    return Order(
        id=row[0], start_address=row[1], final_address=row[2], cost=row[3],
        order_time=row[4], end_time=row[5], car_id=row[6], driver_id=row[7],
        customer_id=row[8], status=Status(row[9])
    )


def get_orders(
        cursor,
        start_address: Optional[str] = None,
        final_address: Optional[str] = None,
        cost: Optional[int] = None,
        order_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        car_id: Optional[int] = None,
        driver_id: Optional[int] = None,
        customer_id: Optional[int] = None,
        status: Optional[Status] = None
) -> List[Order]:
    query = "SELECT * FROM vasilev_goncharov.Orders WHERE 1=1"
    params = []
    if start_address:
        query += " AND start_address = %s"
        params.append(start_address)
    if final_address:
        query += " AND final_address = %s"
        params.append(final_address)
    if cost is not None:
        query += " AND cost = %s"
        params.append(cost)
    if order_time:
        query += " AND order_time = %s"
        params.append(order_time)
    if end_time:
        query += " AND end_time = %s"
        params.append(end_time)
    if car_id is not None:
        query += " AND car_id = %s"
        params.append(car_id)
    if driver_id is not None:
        query += " AND driver_id = %s"
        params.append(driver_id)
    if customer_id is not None:
        query += " AND customer_id = %s"
        params.append(customer_id)
    if status:
        query += " AND status = %s"
        params.append(status.value)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    return [Order(
        id=row[0], start_address=row[1], final_address=row[2], cost=row[3],
        order_time=row[4], end_time=row[5], car_id=row[6], driver_id=row[7],
        customer_id=row[8], status=Status(row[9])
    ) for row in rows]


def update_order(cursor, order_id: int, order_update: OrderUpdate):
    set_clause = []
    params = []
    if order_update.start_address is not None:
        set_clause.append("start_address = %s")
        params.append(order_update.start_address)
    if order_update.final_address is not None:
        set_clause.append("final_address = %s")
        params.append(order_update.final_address)
    if order_update.cost is not None:
        set_clause.append("cost = %s")
        params.append(order_update.cost)
    if order_update.order_time is not None:
        set_clause.append("order_time = %s")
        params.append(order_update.order_time)
    if order_update.end_time is not None:
        set_clause.append("end_time = %s")
        params.append(order_update.end_time)
    if order_update.car_id is not None:
        set_clause.append("car_id = %s")
        params.append(order_update.car_id)
    if order_update.driver_id is not None:
        set_clause.append("driver_id = %s")
        params.append(order_update.driver_id)
    if order_update.customer_id is not None:
        set_clause.append("customer_id = %s")
        params.append(order_update.customer_id)
    if order_update.status is not None:
        set_clause.append("status = %s")
        params.append(order_update.status.value)
    if not set_clause:
        return
    query = "UPDATE vasilev_goncharov.Orders SET " + ", ".join(set_clause) + " WHERE id = %s"
    params.append(order_id)
    cursor.execute(query, params)
    cursor.connection.commit()


def delete_order(cursor, order_id: int) -> Order:
    order = load_order(cursor, order_id)
    cursor.execute("DELETE FROM vasilev_goncharov.Orders WHERE id = %s", (order_id,))
    cursor.connection.commit()
    return order
