import unittest
import tempfile
import os
from src.db.backend.csv_db import CSVTable, CSVDishesTable, CSVOrdersTable
from src.db.backend.errors import FileStorageError, ValidationError

class TestCSVStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filepath = os.path.join(self.temp_dir.name, "test.csv")
        self.fieldnames = ["id", "name", "price"]
        self.table = CSVTable("id", self.filepath, self.fieldnames)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_csv_crud(self):
        self.table.create({"id": 1, "name": "Суп", "price": 12.5})
        self.table.update(1, name="Борщ")
        
        new_table = CSVTable("id", self.filepath, self.fieldnames)
        records = new_table.read()
        self.assertEqual(records[0]["name"], "Борщ")
        
        self.table.delete(1)
        self.assertEqual(len(self.table.read()), 0)

    def test_dishes_and_orders_csv(self):
        dishes_file = os.path.join(self.temp_dir.name, "dishes.csv")
        orders_file = os.path.join(self.temp_dir.name, "orders.csv")
        
        dishes = CSVDishesTable("dish_id", dishes_file, ["dish_id", "price"])
        with self.assertRaises(ValidationError):
            dishes.create({"dish_id": 1, "price": -5})
            
        dishes.create({"dish_id": 1, "price": 10})
        with self.assertRaises(ValidationError):
            dishes.update(1, price=-1)
            
        guests = CSVTable("guest_id", os.path.join(self.temp_dir.name, "guests.csv"), ["guest_id"])
        guests.create({"guest_id": 1})
        
        orders = CSVOrdersTable("order_id", orders_file, ["order_id", "guest_id", "dish_id", "quantity"], guests, dishes)
        
        orders.create({"order_id": 1, "guest_id": 1, "dish_id": 1, "quantity": 2})
        with self.assertRaises(ValidationError):
            orders.create({"order_id": 2, "guest_id": 1, "dish_id": 1, "quantity": -1})
        with self.assertRaises(ValidationError):
            orders.update(1, quantity=-1)

if __name__ == "__main__":
    unittest.main()