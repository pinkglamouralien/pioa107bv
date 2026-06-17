import sys
import os
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from db.backend.json_db import JSONRestaurantDB

class TestJSONDatabase(unittest.TestCase):
    def test_json_data_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "restaurant_test.json")
            
            db1 = JSONRestaurantDB(file_path)
            db1.create_guest(1, "Тест Гость", "123")
            db1.create_dish(1, "Тест Блюдо", 100.0)
            
            db2 = JSONRestaurantDB(file_path)
            guests = db2.read_guests()
            dishes = db2.read_dishes()
            
            self.assertEqual(len(guests), 1)
            self.assertEqual(guests[0].name, "Тест Гость")
            self.assertEqual(len(dishes), 1)
            self.assertEqual(dishes[0].price, 100.0)

if __name__ == "__main__":
    unittest.main()