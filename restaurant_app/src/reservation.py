from .database import get_connection

class ReservationRepo:

    @staticmethod
    def create(customer_id, table_id, date, time):
        conn = get_connection()
        cur = conn.cursor()

        # Check table exists
        cur.execute("SELECT id FROM tables WHERE id=%s", (table_id,))
        if not cur.fetchone():
            raise ValueError("Table not found")

        cur.execute(
            "INSERT INTO reservations (customer_id, table_id, date, time) VALUES (%s, %s, %s, %s)",
            (customer_id, table_id, date, time)
        )
        conn.commit()
        rid = cur.lastrowid
        cur.close()
        conn.close()
        return rid

    @staticmethod
    def list_all():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT r.id, r.date, r.time,
                   c.name AS customer_name,
                   t.number AS table_number
            FROM reservations r
            LEFT JOIN customers c ON c.id = r.customer_id
            LEFT JOIN tables t ON t.id = r.table_id
            ORDER BY r.date DESC, r.time DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def update(reservation_id, customer_id, table_id, date, time):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE reservations SET customer_id=%s, table_id=%s, date=%s, time=%s WHERE id=%s",
            (customer_id, table_id, date, time, reservation_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete(reservation_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM reservations WHERE id=%s", (reservation_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def cancel(reservation_id):
        return ReservationRepo.delete(reservation_id)
