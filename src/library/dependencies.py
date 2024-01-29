from typing import Annotated

import filetype

from fastapi import Depends, UploadFile, HTTPException

from src.library.messages import errors
from src.library.repositories.author_repository import AuthorRepository
from src.library.repositories.book_repository import BookRepository
from src.library.repositories.genre_repository import GenreRepository
from src.library.services.author_service import AuthorService
from src.library.services.book_service import BookService
from src.library.services.genre_service import GenreService
from src.dependencies import AsyncSession
from src.library.services.s3_service import S3Service


def get_genre_repository(db: AsyncSession) -> GenreRepository:
    return GenreRepository(db=db)


GenreRepositoryDep = Annotated[GenreRepository, Depends(get_genre_repository)]


def get_genre_service(repository: GenreRepositoryDep) -> GenreService:
    return GenreService(repository=repository)


GenreServiceDep = Annotated[GenreService, Depends(get_genre_service)]


def get_author_repository(db: AsyncSession) -> AuthorRepository:
    return AuthorRepository(db=db)


AuthorRepositoryDep = Annotated[AuthorRepository, Depends(get_author_repository)]


def get_author_service(repository: AuthorRepositoryDep) -> AuthorService:
    return AuthorService(repository=repository)


AuthorServiceDep = Annotated[AuthorService, Depends(get_author_service)]


def get_book_repository(db: AsyncSession) -> BookRepository:
    return BookRepository(db=db)


BookRepositoryDep = Annotated[BookRepository, Depends(get_book_repository)]


def get_book_service(repository: BookRepositoryDep) -> BookService:
    return BookService(repository=repository)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]


def get_book_pdf_file(file: UploadFile) -> UploadFile:
    file_type = filetype.guess(file.file)

    if file_type is None or file_type.extension.lower() != "pdf":
        raise HTTPException(
            status_code=415,
            detail=errors.BOOK_FILE_HAS_UNSUPPORTED_FILE_TYPE
        )

    return file


BookPDFFile = Annotated[UploadFile, Depends(get_book_pdf_file)]


def get_s3_service() -> S3Service:
    return S3Service()


S3ServiceDep = Annotated[S3Service, Depends(get_s3_service)]
