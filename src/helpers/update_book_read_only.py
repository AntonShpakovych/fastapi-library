from src.dependencies import get_async_session
from src.library.dependencies import get_book_repository, get_book_service
from src.library.schemas.book import BookReadOnlyDTO


async def update_book_read_only(books_title: list[str]) -> None:
    async for session in get_async_session():
        book_repository = get_book_repository(db=session)
        book_service = get_book_service(repository=book_repository)

        for title in books_title:
            book = await book_service.get_book(
                identifier=title,
                raise_exception=False
            )

            if book:
                book.read_only = True
                book = BookReadOnlyDTO.model_validate(book)
                await book_service.update_book(book_id=book.id, new_book=book)
