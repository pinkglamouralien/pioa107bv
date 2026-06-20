import unittest
import tempfile
import os
import json
from src.db.backend.json_db import JSONTable, JSONDishesTable, JSONOrdersTable
from src.db.backend.errors import FileStorageError, ValidationError

class TestJSONStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filepath = os.path.join(self.temp_dir.name, "test.json")
        self.table = JSONTable("id", self.filepath)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_file_crud(self):
        self.table.create({"id": 1, "name": "Иван"})
        self.table.update(1, name="Петр")
        self.assertEqual(self.table.read()[0]["name"], "Петр")
        
        self.table.delete(1)
        self.assertEqual(len(self.table.read()), 0)

    def test_corrupted_file_handling(self):
        with open(self.filepath, "w") as f:
            f.write("{invalid_json:")
        with self.assertRaises(FileStorageError):
            JSONTable("id", self.filepath)

    def test_dishes_and_orders_json(self):
        dishes_file = os.path.join(self.temp_dir.name, "dishes.json")
        orders_file = os.path.join(self.temp_dir.name, "orders.json")
        guests_file = os.path.join(self.temp_dir.name, "guests.json")
        
        dishes = JSONDishesTable("dish_id", dishes_file)
        with self.assertRaises(ValidationError):
            dishes.create({"dish_id": 1, "price": -5})
        
        dishes.create({"dish_id": 1, "price": 10})
        with self.assertRaises(ValidationError):
            dishes.update(1, price=-1)

        guests = JSONTable("guest_id", guests_file)
        guests.create({"guest_id": 1, "name": "Иван"})
        
        orders = JSONOrdersTable("order_id", orders_file, guests, dishes)
        orders.create({"order_id": 1, "guest_id": 1, "dish_id": 1, "quantity": 2})
        
        with self.assertRaises(ValidationError):
            orders.create({"order_id": 2, "guest_id": 1, "dish_id": 1, "quantity": -1})
        with self.assertRaises(ValidationError):
            orders.update(1, quantity=-1)

if __name__ == "__main__":
    unittest.main()