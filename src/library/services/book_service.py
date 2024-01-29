from typing import TYPE_CHECKING

from fastapi import HTTPException
from starlette import status

from src.library.messages import errors
from src.library.models import Book, Author, Genre
from src.library.repositories.book_repository import BookRepository
from src.library.schemas.book import (
    BookInDTO,
    BookUploadFileDTO,
    BookInCreateDTO
)

if TYPE_CHECKING:
    from src.library.services.author_service import AuthorService
    from src.library.services.genre_service import GenreService


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def create_book(
        self,
        book: BookInCreateDTO,
        genre_service: "GenreService",
        author_service: "AuthorService",
    ) -> Book:
        await self._is_book_title_valid(title=book.title)

        book.genres = [
            await genre_service.get_genre(identifier=genre_id)
            for genre_id in book.genres
        ]
        book.authors = [
            await author_service.get_author(author_id=author_id)
            for author_id in book.authors
        ]

        return await self.repository.create(
            book=Book(
                **book.model_dump(),
            )
        )

    async def is_book_valid_for_upload_file(self, book_id: int) -> Book:
        book = await self.get_book(identifier=book_id)

        if book.filename:
            raise HTTPException(
                detail=errors.BOOK_ALREADY_HAS_FILE,
                status_code=400
            )
        return book

    async def delete_book(self, book_id: int) -> None:
        book = await self.get_book(identifier=book_id)
        await self.repository.delete(book=book)

    async def update_book(
        self,
        book_id: int,
        new_book: BookInDTO | BookUploadFileDTO
    ) -> Book:
        book = await self.get_book(identifier=book_id)

        if new_book.title != book.title:
            await self._is_book_title_valid(title=new_book.title)

        return await self.repository.update(
            book_id=book.id,
            new_book=Book(**new_book.model_dump())
        )

    async def get_books(self) -> list[Book]:
        return await self.repository.get_all()

    async def get_book(self, identifier: str | int) -> Book:
        book = (
            await self._get_book_by_title(title=identifier)
            if isinstance(identifier, str)
            else await self._get_book_by_id(book_id=identifier)
        )

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=errors.BOOK_DOESNT_EXIST
            )
        return book

    async def get_book_authors(self, book_id: int) -> list[Author]:
        book = await self.get_book(identifier=book_id)

        return book.authors

    async def get_book_genres(self, book_id: int) -> list[Genre]:
        book = await self.get_book(identifier=book_id)

        return book.genres

    async def update_book_authors(
        self,
        book_id: int,
        authors_id: list[int],
        author_service: "AuthorService"
    ) -> list[Author]:
        book = await self.get_book(identifier=book_id)
        book.authors = [
            await author_service.get_author(author_id=author_id)
            for author_id in authors_id
        ]
        updated_book = await self.repository.update(
            book_id=book.id,
            new_book=book
        )

        return updated_book.authors

    async def update_book_genres(
        self,
        book_id: int,
        genres_id: list[int],
        genre_service: "GenreService"
    ) -> list[Genre]:
        book = await self.get_book(identifier=book_id)
        book.genres = [
            await genre_service.get_genre(identifier=genre_id)
            for genre_id in genres_id
        ]
        updated_book = await self.repository.update(
            book_id=book.id,
            new_book=book
        )

        return updated_book.genres

    async def _get_book_by_title(self, title: str) -> Book | None:
        return await self.repository.get_one(identifier=title)

    async def _get_book_by_id(self, book_id: int) -> Book | None:
        return await self.repository.get_one(identifier=book_id)

    async def _is_book_title_valid(self, title: str) -> None:
        if await self._get_book_by_title(title=title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors.BOOK_TITLE_ALREADY_EXISTS
            )
