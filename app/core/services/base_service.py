# app/core/services/base_service.py

class BaseService:
    def __init__(self, repository):
        self.repository = repository