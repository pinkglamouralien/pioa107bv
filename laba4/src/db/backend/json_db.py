import json
import os
from .errors import FileStorageError, ValidationError
from .memory import Table

class JSONTable(Table):
    def __init__(self, id_field, filename):
        super().__init__(id_field)
        self.filename = filename
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            self._save()
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

                if not isinstance(data, dict):
                    raise FileStorageError(f"Файл {self.filename} имеет неверный формат (ожидался словарь).")
                
                if "records" not in data:
                    raise FileStorageError(f"В файле {self.filename} отсутствует обязательный ключ 'records'.")
                    
                if not isinstance(data["records"], list):
                    raise FileStorageError(f"В файле {self.filename} значение 'records' должно быть списком.")
                
                self.id = data.get("id_field", self.id)
                self.records = data.get("records", [])
                
        except json.JSONDecodeError as e:
            raise FileStorageError(f"Файл {self.filename} поврежден: {e}")
        except OSError as e:
            raise FileStorageError(f"Ошибка доступа к файлу {self.filename}: {e}")

    def _save(self):
        try:
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, 'w', encoding='utf-8') as f:

                json.dump({"id_field": self.id, "records": self.records}, f, ensure_ascii=False, indent=4)
        except OSError as e:
            raise FileStorageError(f"Ошибка сохранения файла {self.filename}: {e}")

    def create(self, record):
        super().create(record)
        self._save()

    def update(self, id_value, **updated_fields):
        super().update(id_value, **updated_fields)
        self._save()

    def delete(self, id_value):
        super().delete(id_value)
        self._save()


class JSONDishesTable(JSONTable):
    def create(self, record):
        if record.get("price", 0) < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        super().create(record)

    def update(self, id_value, **updated_fields):
        if "price" in updated_fields and updated_fields["price"] < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        super().update(id_value, **updated_fields)


class JSONOrdersTable(JSONTable):
    def __init__(self, id_field, filename, guests_table, dishes_table):
        super().__init__(id_field, filename)
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