import csv
import os
from .errors import FileStorageError, ValidationError
from .memory import Table, DishesTable, OrdersTable

class CSVTable(Table):
    def __init__(self, id_field, filename, fieldnames):
        super().__init__(id_field)
        self.filename = filename
        self.fieldnames = fieldnames
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            self._save()
            return
        try:
            with open(self.filename, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                self.records = []
                for row in reader:
                    converted_row = {}
                    for k, v in row.items():
                        if v.isdigit():
                            converted_row[k] = int(v)
                        else:
                            try:
                                converted_row[k] = float(v)
                            except ValueError:
                                converted_row[k] = v
                    self.records.append(converted_row)
        except OSError as e:
            raise FileStorageError(f"Ошибка чтения CSV {self.filename}: {e}")

    def _save(self):
        try:
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(self.records)
        except OSError as e:
            raise FileStorageError(f"Ошибка сохранения CSV {self.filename}: {e}")

    def create(self, record):
        super().create(record)
        self._save()

    def update(self, id_value, **updated_fields):
        super().update(id_value, **updated_fields)
        self._save()

    def delete(self, id_value):
        super().delete(id_value)
        self._save()

class CSVDishesTable(CSVTable):
    def create(self, record):
        if record.get("price", 0) < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        super().create(record)

    def update(self, id_value, **updated_fields):
        if "price" in updated_fields and updated_fields["price"] < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        super().update(id_value, **updated_fields)

class CSVOrdersTable(CSVTable):
    def __init__(self, id_field, filename, fieldnames, guests_table, dishes_table):
        super().__init__(id_field, filename, fieldnames)
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