import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.customer import CustomerRepo, get_connection


class TestCustomerRepo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = get_connection()
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            phone VARCHAR(50)
        );
        """)
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.execute("DROP TABLE IF EXISTS customers;")
        cls.conn.commit()
        cls.cursor.close()
        cls.conn.close()

    def setUp(self):
        self.cursor.execute("DELETE FROM customers;")
        self.conn.commit()

    def test_create_customer(self):
        cid = CustomerRepo.create("Alice", "08123456789")
        self.cursor.execute("SELECT name, phone FROM customers WHERE id=%s", (cid,))
        row = self.cursor.fetchone()
        self.assertEqual(row, ("Alice", "08123456789"))

if __name__ == "__main__":
    unittest.main()
