from fastapi import Depends, HTTPException
from starlette import status

from src.library.messages import errors
from src.library.models import Genre, Book
from src.library.repositories.genre_repository import GenreRepository
from src.library.schemas.genre import GenreInDTO
from src.library.services.book_service import BookService


class GenreService:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    async def create_genre(self, genre: GenreInDTO) -> Genre:
        await self._is_genre_name_valid(name=genre.name)
        return await self.repository.create(genre=Genre(**genre.model_dump()))

    async def get_genres(self) -> list[Genre] | None:
        return await self.repository.get_all()

    async def get_genre(self, identifier: str | int) -> Genre:
        genre = (
            await self._get_genre_by_name(name=identifier)
            if isinstance(identifier, str)
            else await self._get_genre_by_id(genre_id=identifier)
        )

        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=errors.GENRE_DOESNT_EXIST
            )
        return genre

    async def get_genre_books(self, genre_id: int) -> list[Book]:
        genre = await self.get_genre(identifier=genre_id)
        return genre.books

    async def update_genre(
        self,
        genre_id: int,
        new_genre: GenreInDTO
    ) -> Genre:
        genre = await self.get_genre(identifier=genre_id)

        if genre.name != new_genre.name:
            await self._is_genre_name_valid(name=new_genre.name)

        return await self.repository.update(
            identifier=genre.id,
            new_genre=Genre(**new_genre.model_dump())
        )

    async def delete_genre(
        self,
        genre_id: int
    ) -> None:
        genre = await self.get_genre(identifier=genre_id)
        await self.repository.delete(genre=genre)

    async def update_genre_books(
        self,
        genre_id: int,
        books_id: list[int],
        book_service: BookService
    ) -> list[Book]:
        genre = await self.get_genre(identifier=genre_id)
        genre.books = [
            await book_service.get_book(book_id)
            for book_id in books_id
        ]
        updated_genre = await self.repository.update(genre.id, genre)

        return updated_genre.books

    async def _get_genre_by_name(self, name: str) -> Genre | None:
        return await self.repository.get_one(identifier=name)

    async def _get_genre_by_id(self, genre_id: int) -> Genre | None:
        return await self.repository.get_one(identifier=genre_id)

    async def _is_genre_name_valid(self, name: str) -> None:
        if await self._get_genre_by_name(name=name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors.GENRE_NAME_ALREADY_EXISTS
            )
