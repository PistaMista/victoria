from app.services.db import DatabaseService

class TriggerService:
    def __init__(
            self,
            database_service: DatabaseService
        ):
        self._db: DatabaseService = database_service

    def lol(self):
        lol = 1
        
