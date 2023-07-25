from abc import abstractmethod, ABC

from schemas.base import BaseSchema


class BaseCollector(ABC):
    def __init__(self):
        self.storage: list[BaseSchema] = []

    @abstractmethod
    async def fetch(self) -> list:
        raise NotImplementedError

    @abstractmethod
    async def save_to_db(self) -> None:
        raise NotImplementedError
