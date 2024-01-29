from fastapi.responses import JSONResponse
from fastapi import APIRouter
from starlette import status

from celery.result import AsyncResult
from celery_config import app

from src.library.messages import responses


router = APIRouter()


@router.get("/{task_id}")
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
