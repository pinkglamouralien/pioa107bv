type GuestRecord = tuple[int, str, str]

Guests : list[GuestRecord] = []

type DishRecord = tuple[int, str, float]

Dishes : list[DishRecord] = []

type OrderRecord = tuple[int, int, int, int]

Orders : list[OrderRecord] = []

def create_guest (
    guest_id : int,
    name : str,
    phone: str
) -> GuestRecord:
    
    if any(record[0] == guest_id for record in Guests):
        raise ValueError(
            f"Гость с id={guest_id} уже существует"
        )
    
    new_record: GuestRecord = (
        guest_id,
        name.strip(),
        phone.strip()
    )

    Guests.append(new_record)

    return new_record

def read_guests (name: str | None = None):

    if name is None:
        return Guests
    
    return [guest for guest in Guests if guest[1].lower() == name.lower()]

def update_guest(
    guest_id: int,
    new_name: str, 
    new_phone: str
):
    
    for index, guest in enumerate(Guests):
        if guest[0] == guest_id:
            Guests[index] = (
                guest_id,
                new_name.strip(),
                new_phone.strip()
            )

            return

    raise ValueError("Гость не найден.")

def delete_guest(guest_id: int):

    for guest in Guests:
        if guest[0] == guest_id:
            Guests.remove(guest)
            return
    
    raise ValueError("Гость не найден.")

def create_dish(
    dish_id: int,
    name: str,
    price: float
) -> DishRecord:
    
    if price < 0:
        raise ValueError(
            "Цена не может быть отрицательной."
        )
    
    if any(record[0] == dish_id for record in Dishes):
        raise ValueError(
            f"Блюдо c id={dish_id} уже существует."
        )

    new_record: DishRecord = (
        dish_id,
        name.strip(),
        price
    )

    Dishes.append(new_record)

    return new_record

def read_dishes():

    return Dishes

def update_dishes(
    dish_id: int,
    new_name: str,
    new_price: float      
):

    for index, dish in enumerate(Dishes):
        if dish[0] == dish_id:
            Dishes[index] = (
                dish_id,
                new_name.strip(),
                new_price
            )

            return
        
    raise ValueError("Блюдо не найдено.")

def delete_dish(dish_id: int):

    for dish in Dishes:
        if dish[0] == dish_id:
            Dishes.remove(dish)

            return

    raise ValueError("Блюдо не найдено.")

def create_order(
    order_id: int,
    guest_id: int,
    dish_id: int,
    quantity: int
) -> OrderRecord:

    if quantity <= 0:
        raise ValueError(
            "Количество должно быть больше нуля."
        )

    if any(record[0] == order_id for record in Orders):
        raise ValueError(
            f"Заказ с id={order_id} уже существует."
        )

    if not any(record[0] == guest_id for record in Guests):
        raise ValueError("Гость не найден.")

    if not any(record[0] == dish_id for record in Dishes):
        raise ValueError("Блюдо не найдено.")

    new_record: OrderRecord = (
        order_id,
        guest_id,
        dish_id,
        quantity
    )

    Orders.append(new_record)

    return new_record


def read_orders():

    return Orders


def update_order(
    order_id: int,
    quantity: int
):

    for index, order in enumerate(Orders):
        if order[0] == order_id:
            Orders[index] = (
                order[0],
                order[1],
                order[2],
                quantity
            )

            return

    raise ValueError("Заказ не найден.")


def delete_order(order_id: int):

    for order in Orders:
        if order[0] == order_id:
            Orders.remove(order)
            return

    raise ValueError("Заказ не найден.")