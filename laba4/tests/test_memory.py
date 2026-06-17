import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import unittest
from db.backend.memory import RestaurantDB
from db.backend.errors import (DuplicateRecordError, RecordNotFoundError)

class TestRestaurantDB(unittest.TestCase):

    def setUp(self):
        self.db = RestaurantDB()
        self.assertIsInstance(self.db, RestaurantDB)

    def test_create_guest(self):
        cases = [(1, "Иван", "123"), (2, "Петр", "456"), (3, "Анна", "789")]
        for guest_id, name, phone in cases:
            with self.subTest(guest_id=guest_id, name=name):
                guest = self.db.create_guest(guest_id, name, phone)
                self.assertEqual(guest.name, name)

    def test_duplicate_guest(self):
        self.db.create_guest(1, "Иван", "123")
        with self.assertRaises(DuplicateRecordError):
            self.db.create_guest(1, "Петр", "456")
 
    def test_read_guest(self):
        guests = [(1, "Иван", "123"), (2, "Петр", "456"), (3, "Иван", "789")]
        for guest in guests:
            self.db.create_guest(*guest)
        result = self.db.read_guests("Иван")
        self.assertEqual(len(result), 2)

    def test_update_guest(self):
        self.db.create_guest(1, "Иван", "123")
        self.db.update_guest(1, "Петр", "999")
        self.assertEqual(self.db.guests[0].name, "Петр")
        self.assertEqual(self.db.guests[0].phone, "999")

    def test_delete_guest(self):
        self.db.create_guest(1, "Иван", "123")
        self.db.delete_guest(1)
        self.assertEqual(len(self.db.guests), 0)

    def test_guest_not_found(self):
        cases = [100, 200, 300]
        for guest_id in cases:
            with self.subTest(guest_id=guest_id):
                with self.assertRaises(RecordNotFoundError):
                    self.db.delete_guest(guest_id)

    def test_create_dish(self):
        cases = [(1, "Пицца", 20), (2, "Суп", 10), (3, "Салат", 15)]
        for dish_id, name, price in cases:
            with self.subTest(dish_id=dish_id, name=name):
                dish = self.db.create_dish(dish_id, name, price)
                self.assertEqual(dish.price, price)

    def test_negative_price(self):
        cases = [(1, "Пицца", -10), (2, "Суп", -1), (3, "Салат", -100)]
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(ValueError):
                    self.db.create_dish(*test_data)

    def test_create_order(self):
        order = self.db.create_order(1, 1, 1, 2)
        self.assertEqual(order.quantity, 2)

    def test_invalid_order_quantity(self):
        cases = [(1, 1, 1, 0), (2, 1, 1, -1), (3, 1, 1, -5)]
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(ValueError):
                    self.db.create_order(*test_data)

    def test_sort_guests(self):
        guests = [(1, "Сергей", "111"), (2, "Анна", "222"), (3, "Борис", "333")]
        for guest in guests:
            self.db.create_guest(*guest)
        result = self.db.sort_guests("name")
        self.assertEqual(result[0].name, "Анна")
        self.assertEqual(result[1].name, "Борис")
        self.assertEqual(result[2].name, "Сергей")

if __name__ == "__main__":
    unittest.main()