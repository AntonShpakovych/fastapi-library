from sqlalchemy import select, Select
from sqlalchemy.orm import selectinload

from src.library.models import Author
from src.helpers.base_repository import BaseRepository


class AuthorRepository(BaseRepository):
    async def create(self, author: Author) -> Author:
        self.db.add(author)
        await self.db.commit()
        await self.db.refresh(author)

        return author

    async def get_one(
        self,
        first_name: str = None,
        last_name: str = None,
        author_id: int = None
    ) -> Author | None:
        base_stmt = self._prepare_statement_m2m()
        stmt: Select

        if first_name and last_name:
            stmt = base_stmt.filter(
                Author.first_name == first_name,
                Author.last_name == last_name
            )
        else:
            stmt = base_stmt.filter(Author.id == author_id)

        result = await self.db.execute(stmt)
        author = result.scalar_one_or_none()

        return author

    async def get_all(self) -> list[Author] | None:
        stmt = self._prepare_statement_m2m().order_by(Author.id)
        result = await self.db.execute(stmt)
        authors = result.scalars().all()

        return authors

    async def update(self, author_id, new_author: Author) -> Author:
        new_author.id = author_id

        updated_author = await self.db.merge(new_author)
        await self.db.commit()

        return updated_author

    async def delete(self, author: Author) -> None:
        await self.db.delete(author)
        await self.db.commit()

    @staticmethod
    def _prepare_statement_m2m():
        return select(Author).options(
            selectinload(Author.books)
        )
