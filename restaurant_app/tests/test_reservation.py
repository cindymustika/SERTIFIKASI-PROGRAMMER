import sys
import os
import unittest
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.customer import CustomerRepo, get_connection as get_conn_customer
from src.table import TableRepo
from src.reservation import ReservationRepo


class TestReservationRepo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = get_conn_customer()
        cls.cursor = cls.conn.cursor()

        # create customer table
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                phone VARCHAR(50)
            );
        """)

        # create table table
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tables (
                id INT AUTO_INCREMENT PRIMARY KEY,
                number VARCHAR(10),
                capacity INT,
                status VARCHAR(20) DEFAULT 'available'
            );
        """)

        # create reservation table
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                table_id INT,
                date DATE,
                time TIME
            );
        """)
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.execute("DROP TABLE IF EXISTS reservations;")
        cls.cursor.execute("DROP TABLE IF EXISTS tables;")
        cls.cursor.execute("DROP TABLE IF EXISTS customers;")
        cls.conn.commit()
        cls.cursor.close()
        cls.conn.close()

    def setUp(self):
        self.cursor.execute("DELETE FROM reservations;")
        self.cursor.execute("DELETE FROM tables;")
        self.cursor.execute("DELETE FROM customers;")
        self.conn.commit()

    def test_create_reservation(self):
        cid = CustomerRepo.create("Alice", "08123456789")
        tid = TableRepo.create("T1", 4)
        rid = ReservationRepo.create(cid, tid, "2025-12-01", "19:00")
        self.cursor.execute("SELECT customer_id, table_id FROM reservations WHERE id=%s", (rid,))
        row = self.cursor.fetchone()
        self.assertEqual(row, (cid, tid))

    def test_update_reservation(self):
        cid = CustomerRepo.create("Bob", "08123450000")
        tid1 = TableRepo.create("T2", 2)
        tid2 = TableRepo.create("T3", 3)

        # Buat reservasi awal
        rid = ReservationRepo.create(cid, tid1, "2025-12-01", "20:00")

        # Update reservasi
        ReservationRepo.update(rid, cid, tid2, "2025-12-02", "21:00")

        # Ambil data langsung dari DB
        self.cursor.execute(
            "SELECT table_id, date, time FROM reservations WHERE id=%s", (rid,)
        )
        row = self.cursor.fetchone()  # misal: (tid2, date_obj, timedelta_obj)

        table_id, date_db, time_db = row

        # jika time_db berupa timedelta, ubah ke datetime.time
        if isinstance(time_db, timedelta):
            time_db = (datetime.min + time_db).time()

        # assert
        self.assertEqual(table_id, tid2)
        self.assertEqual(date_db, datetime.strptime("2025-12-02", "%Y-%m-%d").date())
        self.assertEqual(time_db, datetime.strptime("21:00", "%H:%M").time())

    def test_cancel_reservation(self):
        cid = CustomerRepo.create("Charlie", "08123451111")
        tid = TableRepo.create("T4", 6)
        rid = ReservationRepo.create(cid, tid, "2025-12-01", "18:00")
        ReservationRepo.cancel(rid)
        self.cursor.execute("SELECT COUNT(*) FROM reservations WHERE id=%s", (rid,))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0)

if __name__ == "__main__":
    unittest.main()
