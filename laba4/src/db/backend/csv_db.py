import csv
from pathlib import Path
from src.db.backend.memory import RestaurantDB, Guest, Dish, Order
from src.db.backend.errors import DatabaseError

class CSVRestaurantDB(RestaurantDB):

    def __init__(self, data_dir: str = "data"):
        super().__init__()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.guests_file = self.data_dir / "guests.csv"
        self.dishes_file = self.data_dir / "dishes.csv"
        self.orders_file = self.data_dir / "orders.csv"
        
        self._load_data()

    def _load_data(self):
        try:
            if self.guests_file.exists():
                with open(self.guests_file, "r", encoding="utf-8", newline="") as f:
                    self.guests = [Guest(int(row["guest_id"]), row["name"], row["phone"]) for row in csv.DictReader(f)]

            if self.dishes_file.exists():
                with open(self.dishes_file, "r", encoding="utf-8", newline="") as f:
                    self.dishes = [Dish(int(row["dish_id"]), row["name"], float(row["price"])) for row in csv.DictReader(f)]

            if self.orders_file.exists():
                with open(self.orders_file, "r", encoding="utf-8", newline="") as f:
                    self.orders = [Order(int(row["order_id"]), int(row["guest_id"]), int(row["dish_id"]), int(row["quantity"])) for row in csv.DictReader(f)]
        except Exception as e:
            raise DatabaseError(f"Ошибка чтения CSV-файлов: {e}")

    def _save_data(self):
        with open(self.guests_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["guest_id", "name", "phone"])
            writer.writeheader()
            for g in self.guests:
                writer.writerow({"guest_id": g.id, "name": g.name, "phone": g.phone})

        with open(self.dishes_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["dish_id", "name", "price"])
            writer.writeheader()
            for d in self.dishes:
                writer.writerow({"dish_id": d.id, "name": d.name, "price": d.price})

        with open(self.orders_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["order_id", "guest_id", "dish_id", "quantity"])
            writer.writeheader()
            for o in self.orders:
                writer.writerow({"order_id": o.id, "guest_id": o.guest_id, "dish_id": o.dish_id, "quantity": o.quantity})

    def create_guest(self, guest_id: int, name: str, phone: str):
        guest = super().create_guest(guest_id, name, phone)
        self._save_data()
        return guest

    def update_guest(self, guest_id: int, name: str, phone: str):
        super().update_guest(guest_id, name, phone)
        self._save_data()

    def delete_guest(self, guest_id: int):
        super().delete_guest(guest_id)
        self._save_data()

    def create_dish(self, dish_id: int, name: str, price: float):
        dish = super().create_dish(dish_id, name, price)
        self._save_data()
        return dish

    def delete_dish(self, dish_id: int):
        super().delete_dish(dish_id)
        self._save_data()

    def create_order(self, order_id: int, guest_id: int, dish_id: int, quantity: int):
        order = super().create_order(order_id, guest_id, dish_id, quantity)
        self._save_data()
        return order

    def delete_order(self, order_id: int):
        super().delete_order(order_id)
        self._save_data()