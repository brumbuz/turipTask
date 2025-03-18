import os
from datetime import datetime

from dotenv import load_dotenv
import psycopg2 as pc
from models.Cars import Car
from models.Customers import Customer
from models.Drivers import Driver
from models.Orders import Order, Status


def get_cursor():
    load_dotenv()
    db = pc.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return db.cursor()


def save_car(stamp: str, number: str):
    cur = get_cursor()
    cur.execute(
        "INSERT INTO vasilev_goncharov.Cars (number, stamp) VALUES (%s, %s)",
        (stamp, number))
    cur.connection.commit()
    cur.close()


def load_car(car_id: int) -> Car:
    cur = get_cursor()
    cur.execute(
        "SELECT * FROM vasilev_goncharov.Cars WHERE id = %s",
        (car_id,))
    id, number, stamp = cur.fetchone()
    car = Car(id=id, numbers=number, stamp=stamp)
    cur.close()
    return car


def save_driver(name: str, birthday: datetime, balance: float, passport: str = None):
    cur = get_cursor()
    cur.execute(
        "INSERT INTO vasilev_goncharov.Drivers (name, birthday, balance, passport) VALUES (%s, %s, %s, %s)",
        (name, birthday, balance, passport)
    )
    cur.connection.commit()
    cur.close()


def load_driver(driver_id: int) -> Driver:
    cur = get_cursor()
    cur.execute("SELECT * FROM vasilev_goncharov.Drivers WHERE id = %s", (driver_id,))
    id, name, birthday, balance, passport = cur.fetchone()
    driver = Driver(id=id, name=name, birthday=birthday, balance=balance, passport=passport)
    cur.close()
    return driver


def save_customer(name: str, birthday: datetime, balance: float):
    cur = get_cursor()
    cur.execute(
        "INSERT INTO vasilev_goncharov.Customers (name, birthday, balance) VALUES (%s, %s, %s)",
        (name, birthday, balance)
    )
    cur.connection.commit()
    cur.close()


def load_customer(customer_id: int) -> Customer:
    cur = get_cursor()
    cur.execute("SELECT * FROM vasilev_goncharov.Customers WHERE id = %s", (customer_id,))
    id, name, birthday, balance = cur.fetchone()
    customer = Customer(id=id, name=name, birthday=birthday, balance=balance)
    cur.close()
    return customer


def save_order(
    start_address: str,
    final_address: str,
    cost: float,
    order_time: datetime,
    end_time: datetime,
    car_id: int,
    driver_id: int,
    customer_id: int,
    status: Status
):
    cur = get_cursor()
    cur.execute(
        """INSERT INTO vasilev_goncharov.Orders 
        (start_address, final_address, cost, order_time, end_time, car_id, driver_id, customer_id, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (start_address, final_address, cost, order_time, end_time, car_id, driver_id, customer_id, status.value)
    )
    cur.connection.commit()
    cur.close()

def load_order(order_id: int) -> Order:
    cur = get_cursor()
    cur.execute("SELECT * FROM vasilev_goncharov.Orders WHERE id = %s", (order_id,))
    id, start_address, final_address, cost, order_time, end_time, car_id, driver_id, customer_id, status = cur.fetchone()
    order = Order(
        id=id,
        start_address=start_address,
        final_address=final_address,
        cost=cost,
        order_time=order_time,
        end_time=end_time,
        car_id=car_id,
        driver_id=driver_id,
        customer_id=customer_id,
        status=Status(status)
    )
    cur.close()
    return order

if __name__ == "__main__":

    save_car("Toyota", "ABC123")
    print("car:", load_car(2))

    driver_birthday = datetime(1990, 1, 1)
    save_driver("John Doe", driver_birthday, 100.0, "P12345")
    print("driver:", load_driver(1))

    customer_birthday = datetime(1995, 5, 5)
    save_customer("Jane Doe", customer_birthday, 50.0)
    print("customer:", load_customer(1))

    order_time = datetime(2023, 1, 1, 10, 0)
    end_time = datetime(2023, 1, 1, 11, 0)
    save_order("Start St", "End St", 25.0, order_time, end_time, 2, 1, 1, Status.pending)
    print("Saved order:", load_order(2))