import unittest
from src.db.backend.memory import Guests, Dishes, Orders
from src.db.backend.errors import RecordNotFoundError, DuplicateRecordError, ValidationError

class TestDatabase(unittest.TestCase):
    def setUp(self):
        Guests.records.clear()
        Dishes.records.clear()
        Orders.records.clear()

    def test_guests_crud_and_sorting(self):
        Guests.create({"guest_id": 1, "name": "Zack", "phone": "123"})
        Guests.create({"guest_id": 2, "name": "Anna", "phone": "456"})
        
        sorted_guests = Guests.read(sort_by="name", reverse=False)
        self.assertEqual(sorted_guests[0]["name"], "Anna")
        
        filtered = Guests.read(name="Zack")
        self.assertEqual(len(filtered), 1)
        
        Guests.update(1, name="Zack Updated")
        self.assertEqual(Guests.read(guest_id=1)[0]["name"], "Zack Updated")
        
        Guests.delete(1)
        self.assertEqual(len(Guests.read()), 1)

    def test_exceptions_thrown(self):
        Guests.create({"guest_id": 1, "name": "Ivan"})
        with self.assertRaises(DuplicateRecordError):
            Guests.create({"guest_id": 1, "name": "Clone"})
        with self.assertRaises(RecordNotFoundError):
            Guests.delete(99)
        with self.assertRaises(RecordNotFoundError):
            Guests.update(99, name="Err")

    def test_dishes_validation(self):
        with self.assertRaises(ValidationError):
            Dishes.create({"dish_id": 1, "price": -5})
        Dishes.create({"dish_id": 2, "price": 10})
        with self.assertRaises(ValidationError):
            Dishes.update(2, price=-10)

    def test_orders_validation(self):
        Guests.create({"guest_id": 1, "name": "Ivan"})
        Dishes.create({"dish_id": 1, "price": 10})
        
        Orders.create({"order_id": 1, "guest_id": 1, "dish_id": 1, "quantity": 2})
        
        with self.assertRaises(ValidationError):
            Orders.create({"order_id": 2, "guest_id": 1, "dish_id": 1, "quantity": 0})
            
        with self.assertRaises(ValidationError):
            Orders.create({"order_id": 3, "guest_id": 99, "dish_id": 1, "quantity": 1})

        with self.assertRaises(ValidationError):
            Orders.update(1, quantity=-5)

if __name__ == "__main__":
    unittest.main()