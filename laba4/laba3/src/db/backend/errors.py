class DatabaseError(Exception):
    """Базовая ошибка базы данных."""

class DuplicateRecordError(DatabaseError):
    """Запись уже существует."""

class RecordNotFoundError(DatabaseError):
    """Запись не найдена."""