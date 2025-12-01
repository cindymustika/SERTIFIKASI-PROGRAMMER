import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.table import TableRepo, get_connection


class TestTableRepo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = get_connection()
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tables (
                id INT AUTO_INCREMENT PRIMARY KEY,
                number VARCHAR(10),
                capacity INT,
                status VARCHAR(20) DEFAULT 'available'
            );
        """)
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.execute("DROP TABLE IF EXISTS tables;")
        cls.conn.commit()
        cls.cursor.close()
        cls.conn.close()

    def setUp(self):
        self.cursor.execute("DELETE FROM tables;")
        self.conn.commit()

    def test_create_table(self):
        tid = TableRepo.create("T1", 4)
        self.cursor.execute("SELECT number, capacity, status FROM tables WHERE id=%s", (tid,))
        row = self.cursor.fetchone()
        self.assertEqual(row, ("T1", 4, "available"))

    def test_update_table(self):
        tid = TableRepo.create("T2", 2)
        TableRepo.update(tid, "T2A", 3, "available")
        self.cursor.execute("SELECT number, capacity FROM tables WHERE id=%s", (tid,))
        row = self.cursor.fetchone()
        self.assertEqual(row, ("T2A", 3))

    def test_delete_table(self):
        tid = TableRepo.create("T3", 6)
        TableRepo.delete(tid)
        self.cursor.execute("SELECT COUNT(*) FROM tables WHERE id=%s", (tid,))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0)

if __name__ == "__main__":
    unittest.main()
