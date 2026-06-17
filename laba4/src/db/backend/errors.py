class DatabaseError(Exception):
    pass

class DuplicateRecordError(DatabaseError):
    pass

class RecordNotFoundError(DatabaseError):
    pass