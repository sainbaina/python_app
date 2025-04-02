import os
import psycopg2
from psycopg2 import sql
from flask import Flask, request, jsonify

app = Flask(__name__)

# Подключение к базе данных
def create_connection():
    conn = psycopg2.connect(
        dbname="mydatabase",  # os.getenv("POSTGRES_DB"),
        user="myuser",  # os.getenv("POSTGRES_USER"),
        password="mypassword",  # os.getenv("POSTGRES_PASSWORD"),
        host="db",  # os.getenv("POSTGRES_HOST"),
        port="5432"  # os.getenv("POSTGRES_PORT")
    )
    return conn

# Создание таблицы
def create_table():
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        ''')
    conn.commit()
    conn.close()

# Добавление пользователя
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")
    age = data.get("age")

    if not name or not age:
        return jsonify({"error": "Missing 'name' or 'age'"}), 400

    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s) RETURNING id;", (name, age))
        user_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({"message": "User added", "id": user_id}), 201

# Просмотр всех пользователей
@app.route("/users", methods=["GET"])
def get_users():
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
    conn.close()

    users = [{"id": row[0], "name": row[1], "age": row[2]} for row in rows]
    return jsonify(users)

@app.route("/")
def home():
    return "Flask App is running inside Docker!"

# Основная функция
if __name__ == "__main__":
    create_table()
    app.run(host="0.0.0.0", port=5000, debug=True)
