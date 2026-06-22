import unittest
from src.db.backend.memory import Table, DishesTable, OrdersTable
from src.db.backend.errors import RecordNotFoundError, DuplicateRecordError, ValidationError

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.guests = Table("guest_id")
        self.dishes = DishesTable("dish_id")
        self.orders = OrdersTable("order_id", self.guests, self.dishes)

    def test_guests_crud_and_sorting(self):
        self.guests.create({"guest_id": 1, "name": "Яков", "phone": "123"})
        self.guests.create({"guest_id": 2, "name": "Анна", "phone": "456"})
        
        sorted_guests = self.guests.read(sort_by="name", reverse=False)
        self.assertEqual(sorted_guests[0]["name"], "Анна")
        
        filtered = self.guests.read(name="Яков")
        self.assertEqual(len(filtered), 1)
        
        self.guests.update(1, name="Яков Обновлен")
        self.assertEqual(self.guests.read(guest_id=1)[0]["name"], "Яков Обновлен")
        
        self.guests.delete(1)
        self.assertEqual(len(self.guests.read()), 1)

    def test_exceptions_thrown(self):
        self.guests.create({"guest_id": 1, "name": "Иван"})
        with self.assertRaises(DuplicateRecordError):
            self.guests.create({"guest_id": 1, "name": "Двойник"})
        with self.assertRaises(RecordNotFoundError):
            self.guests.delete(99)
        with self.assertRaises(RecordNotFoundError):
            self.guests.update(99, name="Ошибка")

    def test_dishes_validation(self):
        with self.assertRaises(ValidationError):
            self.dishes.create({"dish_id": 1, "price": -5})
        self.dishes.create({"dish_id": 2, "price": 10})
        with self.assertRaises(ValidationError):
            self.dishes.update(2, price=-10)

    def test_orders_validation(self):
        self.guests.create({"guest_id": 1, "name": "Иван"})
        self.dishes.create({"dish_id": 1, "price": 10})
        
        self.orders.create({"order_id": 1, "guest_id": 1, "dish_id": 1, "quantity": 2})
        
        with self.assertRaises(ValidationError):
            self.orders.create({"order_id": 2, "guest_id": 1, "dish_id": 1, "quantity": 0})
            
        with self.assertRaises(ValidationError):
            self.orders.create({"order_id": 3, "guest_id": 99, "dish_id": 1, "quantity": 1})

        with self.assertRaises(ValidationError):
            self.orders.update(1, quantity=-5)

if __name__ == "__main__":
    unittest.main()