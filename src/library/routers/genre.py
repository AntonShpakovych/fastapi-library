from fastapi import APIRouter, Depends
from starlette import status

from src.auth.dependencies import admin_current_user
from src.library.schemas.book import BookOutDTO
from src.library.schemas.genre import (
    GenreOutDTO,
    GenreInDTO,
    GenreOutDetailDTO
)
from src.library.dependencies import GenreServiceDep, BookServiceDep

router = APIRouter()


@router.post(
    "/",
    response_model=GenreOutDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_current_user)]
)
async def create_genre(
    genre: GenreInDTO,
    genre_service: GenreServiceDep,
):
    return await genre_service.create_genre(genre=genre)


@router.get(
    "/{genre_id}",
    response_model=GenreOutDetailDTO,
    status_code=status.HTTP_200_OK
)
async def get_genre_by_id(genre_id: int, genre_service: GenreServiceDep):
    return await genre_service.get_genre(identifier=genre_id)


@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(admin_current_user)]
)
async def delete_genre_by_id(genre_id: int, genre_service: GenreServiceDep):
    await genre_service.delete_genre(genre_id=genre_id)


@router.get(
    "/{genre_id}/books",
    response_model=list[BookOutDTO],
    status_code=status.HTTP_200_OK
)
async def get_genre_books(genre_id: int, genre_service: GenreServiceDep):
    return await genre_service.get_genre_books(genre_id=genre_id)


@router.put(
    "/{genre_id}/books",
    response_model=list[BookOutDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_current_user)]
)
async def update_genre_books(
    genre_id: int,
    books_id: list[int],
    genre_service: GenreServiceDep,
    book_service: BookServiceDep
):
    return await genre_service.update_genre_books(
        genre_id=genre_id,
        books_id=books_id,
        book_service=book_service
    )


@router.get(
    "/",
    response_model=list[GenreOutDTO],
    status_code=status.HTTP_200_OK
)
async def get_genres(genre_service: GenreServiceDep):
    return await genre_service.get_genres()


@router.put(
    "/{genre_id}",
    response_model=GenreOutDTO,
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_200_OK
)
async def update_genre(
    genre_id: int,
    new_genre: GenreInDTO,
    genre_service: GenreServiceDep,
):
    return await genre_service.update_genre(
        genre_id=genre_id,
        new_genre=new_genre,
    )
