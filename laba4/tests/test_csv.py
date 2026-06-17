import sys
import os
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from db.backend.csv_db import CSVRestaurantDB

class TestCSVDatabase(unittest.TestCase):
    def test_csv_data_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db1 = CSVRestaurantDB(tmpdir)
            db1.create_guest(1, "Тест Гость", "123")
            
            db2 = CSVRestaurantDB(tmpdir)
            guests = db2.read_guests()
            
            self.assertEqual(len(guests), 1)
            self.assertEqual(guests[0].name, "Тест Гость")

if __name__ == "__main__":
    unittest.main()