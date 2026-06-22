from .errors import RecordNotFoundError, DuplicateRecordError, ValidationError

class Table:
    def __init__(self, id_field):
        self.id = id_field
        self.records = []

    def create(self, record):
        if self.id not in record:
            raise ValidationError(f"Отсутствует обязательное поле: {self.id}")
        if any(r[self.id] == record[self.id] for r in self.records):
            raise DuplicateRecordError(f"Запись с таким ID уже существует.")
        self.records.append(record)

    def read(self, sort_by=None, reverse=False, **filters):
        result = [record for record in self.records if all(str(record.get(k)).lower() == str(v).lower() for k, v in filters.items())]

        if sort_by:
            with_field = [r for r in result if sort_by in r]
            without_field = [r for r in result if sort_by not in r]
            
            with_field.sort(key=lambda x: x[sort_by], reverse=reverse)
            result = with_field + without_field
            
        return result

    def update(self, id_value, **updated_fields):
        if self.id in updated_fields and updated_fields[self.id] != id_value:
            new_id = updated_fields[self.id]
            if any(r[self.id] == new_id for r in self.records):
                raise DuplicateRecordError(f"Запись с ID {new_id} уже существует.")
            
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
    def __init__(self, id_field, guests_table, dishes_table):
        super().__init__(id_field)
        self.guests = guests_table
        self.dishes = dishes_table

    def create(self, record):
        if record.get("quantity", 0) <= 0:
            raise ValidationError("Количество должно быть больше нуля.")
        if not self.guests.read(guest_id=record.get("guest_id")):
            raise ValidationError("Гость не найден.")
        if not self.dishes.read(dish_id=record.get("dish_id")):
            raise ValidationError("Блюдо не найдено.")
        super().create(record)

    def update(self, id_value, **updated_fields):
        if "quantity" in updated_fields and updated_fields["quantity"] <= 0:
            raise ValidationError("Количество должно быть больше нуля.")
        super().update(id_value, **updated_fields)