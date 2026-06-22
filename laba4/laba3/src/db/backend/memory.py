from db.backend.errors import (DuplicateRecordError, RecordNotFoundError)

class Guest:

    def __init__(
        self,
        guest_id: int,
        name: str,
        phone: str
    ):
        self.id = guest_id
        self.name = name
        self.phone = phone

    def __str__(self):
        return (
            f"Guest(id={self.id}, "
            f"name='{self.name}', "
            f"phone='{self.phone}')"
        )

class Dish:

    def __init__(
        self,
        dish_id: int,
        name: str,
        price: float
    ):
        self.id = dish_id
        self.name = name
        self.price = price

    def __str__(self):
        return (
            f"Dish(id={self.id}, "
            f"name='{self.name}', "
            f"price={self.price})"
        )


class Order:

    def __init__(
        self,
        order_id: int,
        guest_id: int,
        dish_id: int,
        quantity: int
    ):
        self.id = order_id
        self.guest_id = guest_id
        self.dish_id = dish_id
        self.quantity = quantity

    def __str__(self):
        return (
            f"Order(id={self.id}, "
            f"guest_id={self.guest_id}, "
            f"dish_id={self.dish_id}, "
            f"quantity={self.quantity})"
        )


class RestaurantDB:

    def __init__(self):
        self.guests = []
        self.dishes = []
        self.orders = []

    def create_guest(
        self,
        guest_id: int,
        name: str,
        phone: str
    ):

        if any(guest.id == guest_id for guest in self.guests):
            raise DuplicateRecordError(f"Гость с id={guest_id} уже существует.")

        guest = Guest(
            guest_id,
            name.strip(),
            phone.strip()
        )

        self.guests.append(guest)

        return guest

    def read_guests(
        self,
        name: str | None = None
    ):

        if name is None:
            return self.guests

        return [guest for guest in self.guests if guest.name.lower() == name.lower()]

    def update_guest(
        self,
        guest_id: int,
        name: str,
        phone: str
    ):

        for guest in self.guests:
            if guest.id == guest_id:
                guest.name = name
                guest.phone = phone
                return

        raise RecordNotFoundError("Гость не найден.")

    def delete_guest(
        self,
        guest_id: int
    ):

        for guest in self.guests:
            if guest.id == guest_id:
                self.guests.remove(guest)
                return

        raise RecordNotFoundError("Гость не найден.")

    def sort_guests(
        self,
        field: str,
        reverse=False
    ):

        return sorted(
            self.guests,
            key=lambda guest: getattr(guest, field),
            reverse=reverse
        )

    def create_dish(
        self,
        dish_id: int,
        name: str,
        price: float
    ):

        if price < 0:
            raise ValueError("Цена не может быть отрицательной.")

        if any(dish.id == dish_id for dish in self.dishes):
            raise DuplicateRecordError(f"Блюдо с id={dish_id} уже существует.")

        dish = Dish(
            dish_id,
            name.strip(),
            price
        )

        self.dishes.append(dish)

        return dish

    def read_dishes(self):
        return self.dishes

    def delete_dish(
        self,
        dish_id: int
    ):

        for dish in self.dishes:
            if dish.id == dish_id:
                self.dishes.remove(dish)
                return

        raise RecordNotFoundError("Блюдо не найдено.")

    def create_order(
        self,
        order_id: int,
        guest_id: int,
        dish_id: int,
        quantity: int
    ):

        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля.")

        order = Order(
            order_id,
            guest_id,
            dish_id,
            quantity
        )

        self.orders.append(order)

        return order

    def read_orders(self):
        return self.orders

    def delete_order(
        self,
        order_id: int
    ):

        for order in self.orders:
            if order.id == order_id:
                self.orders.remove(order)
                return

        raise RecordNotFoundError("Заказ не найден.")