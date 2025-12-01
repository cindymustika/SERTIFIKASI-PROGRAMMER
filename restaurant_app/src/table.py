from .database import get_connection

class TableRepo:

    @staticmethod
    def create(number, capacity):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tables (number, capacity, status) VALUES (%s, %s, %s)",
            (number, capacity, "available")
        )
        conn.commit()
        tid = cur.lastrowid
        cur.close()
        conn.close()
        return tid

    @staticmethod
    def list_all():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM tables ORDER BY number")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def list_available():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM tables WHERE status='available' ORDER BY number")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def update(table_id, number, capacity, status):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE tables SET number=%s, capacity=%s, status=%s WHERE id=%s",
            (number, capacity, status, table_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete(table_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tables WHERE id=%s", (table_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def set_booked(table_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE tables SET status='booked' WHERE id=%s", (table_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def set_available(table_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE tables SET status='available' WHERE id=%s", (table_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_id_by_number(number):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM tables WHERE number=%s", (number,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return row[0]
        return None
