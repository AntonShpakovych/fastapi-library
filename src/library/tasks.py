from asyncio import get_event_loop
from botocore.exceptions import ClientError

from celery_config import app

from src.library.messages import responses
from src.library.services.s3_service import S3Service

from src.helpers.update_book_filename import update_book_filename


loop = get_event_loop()


@app.task()
def upload_book_file_to_s3(
        file: bytes,
        filename: str,
        book_id: int,

) -> str:
    s3_service = S3Service()

    try:
        s3_service.upload_file(file=file, filename=filename)

        loop.run_until_complete(
            update_book_filename(
                book_id=book_id,
                filename=filename
            )
        )

        return responses.S3_BOOK_FILE_SUCCESSFULLY_UPLOADED
    except ClientError as error:
        return str(error)
