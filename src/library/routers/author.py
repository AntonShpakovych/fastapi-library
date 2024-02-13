from fastapi import APIRouter, Depends
from starlette import status

from src.auth.dependencies import admin_current_user
from src.library.dependencies import AuthorServiceDep, BookServiceDep
from src.library.schemas.author import (
    AuthorOutDTO,
    AuthorInDTO,
    AuthorOutDetailDTO
)
from src.library.schemas.book import BookOutDTO

router = APIRouter()


@router.post(
    "/",
    response_model=AuthorOutDTO,
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_201_CREATED
)
async def create_author(author: AuthorInDTO, author_service: AuthorServiceDep):
    return await author_service.create_author(author=author)


@router.get(
    "/",
    response_model=list[AuthorOutDTO],
    status_code=status.HTTP_200_OK
)
async def get_authors(author_service: AuthorServiceDep):
    return await author_service.get_authors()


@router.get(
    "/{author_id}",
    response_model=AuthorOutDetailDTO,
    status_code=status.HTTP_200_OK
)
async def get_author_by_id(author_id: int, author_service: AuthorServiceDep):
    return await author_service.get_author(author_id=author_id)


@router.get(
    "/{author_id}/books",
    response_model=list[BookOutDTO],
    status_code=status.HTTP_200_OK
)
async def get_author_books(author_id: int, author_service: AuthorServiceDep):
    return await author_service.get_author_books(author_id=author_id)


@router.put(
    "/{author_id}",
    response_model=AuthorOutDTO,
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_200_OK
)
async def update_author_by_id(
    author_id: int,
    author: AuthorInDTO,
    author_service: AuthorServiceDep
):
    return await author_service.update_author(
        author_id=author_id,
        new_author=author
    )


@router.delete(
    "/{author_id}",
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_author_by_id(
    author_id: int,
    author_service: AuthorServiceDep
):
    await author_service.delete_author(author_id=author_id)


@router.put(
    "/{author_id}/books",
    response_model=list[BookOutDTO],
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_200_OK
)
async def update_author_books(
        author_id: int,
        books_id: list[int],
        author_service: AuthorServiceDep,
        book_service: BookServiceDep
):
    return await author_service.update_author_books(
        author_id=author_id,
        books_id=books_id,
        book_service=book_service
    )
