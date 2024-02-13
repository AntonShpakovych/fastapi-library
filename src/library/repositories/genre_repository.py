from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.library.models import Genre
from src.helpers.base_repository import BaseRepository


class GenreRepository(BaseRepository):
    async def create(self, genre: Genre) -> Genre:
        self.db.add(genre)
        await self.db.commit()
        await self.db.refresh(genre)

        return genre

    async def get_one(self, identifier: str | int) -> Genre | None:
        base_stmt = self._prepare_statement_m2m()
        stmt = (
            base_stmt
            .filter(Genre.id == identifier)
            if isinstance(identifier, int)
            else base_stmt.filter(Genre.name == identifier)
        )

        result = await self.db.execute(stmt)
        genre = result.scalar_one_or_none()

        return genre

    async def get_all(self) -> list[Genre] | None:
        stmt = self._prepare_statement_m2m().order_by(Genre.id)
        result = await self.db.execute(stmt)
        genres = result.scalars().all()

        return genres

    async def update(self, identifier: int, new_genre: Genre) -> Genre:
        new_genre.id = identifier

        updated_genre = await self.db.merge(new_genre)
        await self.db.commit()

        return updated_genre

    async def delete(self, genre: Genre) -> None:
        await self.db.delete(genre)
        await self.db.commit()

    @staticmethod
    def _prepare_statement_m2m():
        return select(Genre).options(
            selectinload(Genre.books)
        )
