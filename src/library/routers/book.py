from fastapi import APIRouter, Depends

from starlette import status
from starlette.responses import Response

from src.auth.dependencies import admin_current_user, current_user
from src.library.dependencies import (
    BookServiceDep,
    AuthorServiceDep,
    GenreServiceDep,
    BookPDFFile, S3ServiceDep
)
from src.library.messages import responses
from src.library.schemas.author import AuthorOutDTO
from src.library.schemas.book import (
    BookOutDTO,
    BookOutDetailDTO,
    BookInCreateDTO,
    BookInUpdateDTO
)

from src.library.schemas.genre import GenreOutDTO
from src.library.tasks import upload_book_file_to_s3


router = APIRouter()


@router.get(
    "/",
    response_model=list[BookOutDTO],
    status_code=status.HTTP_200_OK
)
async def get_books(book_service: BookServiceDep):
    return await book_service.get_books()


@router.post(
    "/",
    response_model=BookOutDTO,
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_201_CREATED
)
async def create_book(
        book_service: BookServiceDep,
        genre_service: GenreServiceDep,
        author_service: AuthorServiceDep,
        book: BookInCreateDTO,
):
    return await book_service.create_book(
        book=book,
        genre_service=genre_service,
        author_service=author_service,
    )


@router.put(
    "/{book_id}",
    response_model=BookOutDetailDTO,
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_200_OK
)
async def update_book_by_id(
    book_id: int,
    new_book: BookInUpdateDTO,
    book_service: BookServiceDep
):
    return await book_service.update_book(
        book_id=book_id,
        new_book=new_book
    )


@router.get(
    "/{book_id}",
    response_model=BookOutDetailDTO,
    status_code=status.HTTP_200_OK
)
async def get_book_by_id(book_id: int, book_service: BookServiceDep):
    return await book_service.get_book(identifier=book_id)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(admin_current_user)]
)
async def delete_book_by_id(book_id: int, book_service: BookServiceDep):
    await book_service.delete_book(book_id=book_id)


@router.get(
    "/{book_id}/authors",
    response_model=list[AuthorOutDTO],
    status_code=status.HTTP_200_OK
)
async def get_book_authors(
    book_id: int,
    book_service: BookServiceDep,
):
    return await book_service.get_book_authors(book_id=book_id)


@router.get(
    "/{book_id}/genres",
    response_model=list[GenreOutDTO],
    status_code=status.HTTP_200_OK
)
async def get_book_genres(
    book_id: int,
    book_service: BookServiceDep,
):
    return await book_service.get_book_genres(book_id=book_id)


@router.put(
    "/{book_id}/authors",
    response_model=list[AuthorOutDTO],
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_200_OK
)
async def update_book_authors(
    book_id: int,
    authors_id: list[int],
    book_service: BookServiceDep,
    author_service: AuthorServiceDep
):
    return await book_service.update_book_authors(
        book_id=book_id,
        authors_id=authors_id,
        author_service=author_service
    )


@router.put(
    "/{book_id}/genres",
    response_model=list[GenreOutDTO],
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_200_OK
)
async def update_book_genres(
    book_id: int,
    genres_id: list[int],
    book_service: BookServiceDep,
    genre_service: GenreServiceDep
):
    return await book_service.update_book_genres(
        book_id=book_id,
        genres_id=genres_id,
        genre_service=genre_service
    )


@router.post(
    "/{book_id}/upload",
    dependencies=[Depends(admin_current_user)],
    status_code=status.HTTP_200_OK
)
async def upload_file_for_book(
        book_id: int,
        book_service: BookServiceDep,
        file: BookPDFFile
):
    book = await book_service.is_book_valid_for_upload_file(book_id=book_id)

    filename = file.filename
    file = await file.read()

    task = upload_book_file_to_s3.delay(
        file=file,
        filename=filename,
        book_id=book.id
    )

    return {"detail": responses.WE_ARE_PROCESSING_YOUR_FILE + task.id}


@router.get("/{book_id}/pdf", dependencies=[Depends(current_user)])
async def download_file_for_book(
    book_id: int,
    s3_service: S3ServiceDep,
    book_service: BookServiceDep
):
    book = await book_service.get_book(identifier=book_id)

    response = s3_service.download_file(filename=book.filename)
    body = response["Body"].read()
    headers = {
        "Content-Disposition": f"attachment; filename={book.filename}",
    }
    return Response(
        content=body,
        headers=headers,
        media_type="application/pdf",
    )
