from .errors import RecordNotFoundError, DuplicateRecordError, ValidationError

class Table:
    def __init__(self, id):
        self.id = id
        self.records = []

    def create(self, record):
        if any(r[self.id] == record[self.id] for r in self.records):
            raise DuplicateRecordError("Запись с таким ID уже существует.")
        self.records.append(record)

    def read(self, sort_by=None, reverse=False, **filters):
        result = [record for record in self.records if all(str(record.get(k)).lower() == str(v).lower() for k, v in filters.items())]

        if sort_by:
            result = sorted(result, key=lambda x: str(x.get(sort_by, "")), reverse=reverse)
            
        return result

    def update(self, id_value, **updated_fields):
        for record in self.records:
            if record[self.id] == id_value:
                record.update(updated_fields)
                return
        raise RecordNotFoundError("Запись не найдена.")

    def delete(self, id_value):
        for record in self.records:
            if record[self.id] == id_value:
                self.records.remove(record)
                return
        raise RecordNotFoundError("Запись не найдена.")


class DishesTable(Table):
    def create(self, record):
        if record.get("price", 0) < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        super().create(record)

    def update(self, id_value, **updated_fields):
        if "price" in updated_fields and updated_fields["price"] < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        super().update(id_value, **updated_fields)


class OrdersTable(Table):
    def create(self, record):
        if record.get("quantity", 0) <= 0:
            raise ValidationError("Количество должно быть больше нуля.")
        
        if not Guests.read(guest_id=record.get("guest_id")):
            raise ValidationError("Гость не найден.")
        if not Dishes.read(dish_id=record.get("dish_id")):
            raise ValidationError("Блюдо не найдено.")
            
        super().create(record)

    def update(self, id_value, **updated_fields):
        if "quantity" in updated_fields and updated_fields["quantity"] <= 0:
            raise ValidationError("Количество должно быть больше нуля.")
        super().update(id_value, **updated_fields)

Guests = Table("guest_id")
Dishes = DishesTable("dish_id")
Orders = OrdersTable("order_id")