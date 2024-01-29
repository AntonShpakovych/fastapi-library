from fastapi import HTTPException
from starlette import status

from src.library.messages import errors
from src.library.models import Author, Book
from src.library.repositories.author_repository import AuthorRepository
from src.library.schemas.author import AuthorInDTO
from src.library.services.book_service import BookService


class AuthorService:
    def __init__(self, repository: AuthorRepository):
        self.repository = repository

    async def create_author(self, author: AuthorInDTO) -> Author:
        await self._is_author_fullname_valid(
            first_name=author.first_name,
            last_name=author.last_name
        )

        return await self.repository.create(
            author=Author(**author.model_dump())
        )

    async def get_authors(self) -> list[Author] | None:
        return await self.repository.get_all()

    async def get_author(
        self,
        first_name: str = None,
        last_name: str = None,
        author_id: int = None
    ) -> Author:
        author = (
            await self._get_author_by_fullname(
                first_name=first_name,
                last_name=last_name
            )
            if first_name and last_name else
            await self._get_author_by_id(author_id=author_id)
        )

        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=errors.AUTHOR_DOESNT_EXIST
            )
        return author

    async def update_author(
        self,
        author_id: int,
        new_author: AuthorInDTO
    ) -> Author:
        author = await self.get_author(author_id=author_id)
        if (
            new_author.first_name != author.first_name
            or new_author.last_name != author.last_name
        ):
            await self._is_author_fullname_valid(
                first_name=new_author.first_name,
                last_name=new_author.last_name
            )

        return await self.repository.update(
            author_id=author.id,
            new_author=Author(**new_author.model_dump())
        )

    async def delete_author(self, author_id: int) -> None:
        author = await self.get_author(author_id=author_id)
        await self.repository.delete(author=author)

    async def update_author_books(
        self,
        author_id: int,
        books_id: list[int],
        book_service: BookService
    ) -> list[Book]:
        author = await self.get_author(author_id=author_id)
        author.books = [
            await book_service.get_book(identifier=book_id)
            for book_id in books_id
        ]
        updated_author = await self.repository.update(
            author_id=author.id,
            new_author=author
        )

        return updated_author.books

    async def get_author_books(self, author_id: int) -> list[Book]:
        author = await self.get_author(author_id=author_id)
        return author.books

    async def _get_author_by_fullname(
        self,
        first_name: str,
        last_name: str
    ) -> Author | None:
        return await self.repository.get_one(
            first_name=first_name,
            last_name=last_name
        )

    async def _get_author_by_id(self, author_id: int) -> Author | None:
        return await self.repository.get_one(author_id=author_id)

    async def _is_author_fullname_valid(
        self,
        first_name: str,
        last_name: str
    ) -> None:
        if await self._get_author_by_fullname(
                first_name=first_name,
                last_name=last_name
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors.AUTHOR_ALREADY_EXISTS
            )
