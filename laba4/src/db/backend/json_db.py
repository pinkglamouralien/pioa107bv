import json
from pathlib import Path
from src.db.backend.memory import RestaurantDB, Guest, Dish, Order
from src.db.backend.errors import DatabaseError

class JSONRestaurantDB(RestaurantDB):

    def __init__(self, file_path: str = "data/restaurant.json"):
        super().__init__()
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._load_data()

    def _load_data(self):
        if not self.file_path.exists():
            return
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                self.guests = [Guest(g["guest_id"], g["name"], g["phone"]) for g in data.get("guests", [])]
                self.dishes = [Dish(d["dish_id"], d["name"], d["price"]) for d in data.get("dishes", [])]
                self.orders = [Order(o["order_id"], o["guest_id"], o["dish_id"], o["quantity"]) for o in data.get("orders", [])]
        except (json.JSONDecodeError, KeyError, TypeError):
            raise DatabaseError("Файл базы данных поврежден или имеет неверный формат.")

    def _save_data(self):
        data = {
            "guests": [{"guest_id": g.id, "name": g.name, "phone": g.phone} for g in self.guests],
            "dishes": [{"dish_id": d.id, "name": d.name, "price": d.price} for d in self.dishes],
            "orders": [{"order_id": o.id, "guest_id": o.guest_id, "dish_id": o.dish_id, "quantity": o.quantity} for o in self.orders]
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

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