from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.library.models import Book
from src.helpers.base_repository import BaseRepository


class BookRepository(BaseRepository):
    async def create(self, book: Book) -> Book:
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)

        return book

    async def get_all(self) -> list[Book] | None:
        stmt = self._prepare_statement_m2m().order_by(Book.id)
        result = await self.db.execute(stmt)
        books = result.scalars().all()

        return books

    async def get_one(self, identifier: str | int) -> Book | None:
        base_stmt = self._prepare_statement_m2m()
        stmt = (
            base_stmt
            .filter(Book.id == identifier)
            if isinstance(identifier, int)
            else base_stmt.filter(Book.title == identifier)
        )

        result = await self.db.execute(stmt)
        book = result.scalar_one_or_none()

        return book

    async def update(self, book_id: int, new_book: Book) -> Book:
        new_book.id = book_id

        updated_book = await self.db.merge(new_book)
        await self.db.commit()

        return updated_book

    async def delete(self, book: Book) -> None:
        await self.db.delete(book)
        await self.db.commit()

    @staticmethod
    def _prepare_statement_m2m():
        return select(Book).options(
            selectinload(Book.genres),
            selectinload(Book.authors)
        )
