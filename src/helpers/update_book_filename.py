from src.library.dependencies import get_book_repository, get_book_service
from src.library.schemas.book import BookUploadFileDTO
from src.dependencies import get_async_session


async def update_book_filename(book_id: int, filename: str):
    async for session in get_async_session():
        book_repository = get_book_repository(db=session)
        book_service = get_book_service(repository=book_repository)
        book = await book_service.get_book(identifier=book_id)
        book.filename = filename
        book = BookUploadFileDTO.model_validate(book)
        await book_service.update_book(book_id=book_id, new_book=book)
