# src/reporting.py
from .database import get_connection

class ReportingRepo:

    @staticmethod
    def total_customers():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customers")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count

    @staticmethod
    def total_tables():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tables")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count

    @staticmethod
    def total_reservations():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM reservations")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count
