class DBError(Exception):
    pass

class RecordNotFoundError(DBError):
    pass

class DuplicateRecordError(DBError):
    pass

class ValidationError(DBError):
    pass

class FileStorageError(DBError):
    pass