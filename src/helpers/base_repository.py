from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base


class BaseRepository(ABC):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractmethod
    async def create(self, *args, **kwargs) -> Base:
        pass

    @abstractmethod
    async def get_one(self, *args, **kwargs) -> Base | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Base]:
        pass

    async def update(self, *args, **kwargs) -> Base:
        pass
