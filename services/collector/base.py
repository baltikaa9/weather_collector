from schemas.base import BaseSchema


class BaseCollector:
    def __init__(self):
        self.storage: list[BaseSchema] = []

    async def fetch(self) -> list:
        ...

    async def save_to_db(self) -> None:
        ...
