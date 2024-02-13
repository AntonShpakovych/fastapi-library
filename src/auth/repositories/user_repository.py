from sqlalchemy import select

from src.auth.models import User
from src.helpers.base_repository import BaseRepository


class UserRepository(BaseRepository):
    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def get_one(self, identifier: str | int) -> User | None:
        stmt = (
            select(User)
            .filter(User.id == identifier)
            if isinstance(identifier, int)
            else select(User).filter(User.email == identifier)
        )

        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        return user

    async def get_all(self) -> list[User]:
        stmt = select(User).order_by(User.id)

        result = await self.db.execute(stmt)
        users = result.scalars().all()

        return users

    async def update(self, user_id: int, new_user: User) -> User:
        new_user.id = user_id

        await self.db.merge(new_user)
        await self.db.commit()

        return new_user
