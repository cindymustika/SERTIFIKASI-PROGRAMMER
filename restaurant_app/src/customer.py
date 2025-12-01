from .database import get_connection

class CustomerRepo:

    @staticmethod
    def create(name, phone):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers (name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        cid = cur.lastrowid
        cur.close()
        conn.close()
        return cid

    @staticmethod
    def list_all():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM customers ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def update(customer_id, name, phone):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE customers SET name=%s, phone=%s WHERE id=%s",
            (name, phone, customer_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete(customer_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE id=%s", (customer_id,))
        conn.commit()
        cur.close()
        conn.close()
