import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # kalau MySQL kamu pakai password → isi di sini
        database="restaurant"
    )
