from sqlalchemy import select

from src.dependencies import AsyncSession
from src.auth.models import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def get(self, identifier: str | int) -> User | None:
        stmt = (
            select(User)
            .filter(User.id == identifier)
            if isinstance(identifier, int)
            else select(User).filter(User.email == identifier)
        )

        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        return user
