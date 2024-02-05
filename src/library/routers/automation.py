from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from starlette import status

from celery.result import AsyncResult
from celery_config import app
from src.auth.dependencies import admin_current_user

from src.library.messages import responses
from src.library.dependencies import DeniedFileXLS
from src.library.tasks import parse_file_and_add_books_to_denied_books


router = APIRouter()


@router.get("/tasks/{task_id}", dependencies=[Depends(admin_current_user)])
async def task_status(task_id: str):
    task = AsyncResult(task_id, app=app)
    content = (
        task.get() if task.ready()
        else responses.TASK_IS_PROCESSING
    )
    status_code = (
        status.HTTP_200_OK if task.ready()
        else status.HTTP_202_ACCEPTED
    )

    return JSONResponse(content=content, status_code=status_code)


@router.post("/denied_book/", dependencies=[Depends(admin_current_user)])
async def denied_book(denied_books_file: DeniedFileXLS):
    file_bytes = await denied_books_file.read()
    task = parse_file_and_add_books_to_denied_books.delay(
        denied_books_bytes=file_bytes
    )
    return {"detail": responses.WE_ARE_PROCESSING_YOUR_FILE + task.id}
