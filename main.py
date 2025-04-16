import os
import psycopg2 as pc
from dotenv import load_dotenv

load_dotenv()

# Подключение к БД
db = pc.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

with open('migrations/1.0_migrations.sql', 'r', encoding='utf-8') as f:
    sql_commands = f.read()

commands = sql_commands.split(';')

for command in commands:
    command = command.strip()
    if command:
        cursor.execute(command)
        print(f"Выполнена команда: {command}")

db.commit()
db.close()

print("Все миграции успешно выполнены")



