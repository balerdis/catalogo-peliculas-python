# app/core/exceptions/domain/duplicate_entry.py
class DuplicateEntityError(Exception):
    def __init__(self, entity: str, field: str, value: str):
        self.entity = entity
        self.field = field
        self.value = value
        super().__init__(f"{entity} with {field}='{value}' already exists")