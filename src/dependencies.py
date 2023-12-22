from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession as AsyncLocalSession

from fastapi import Depends

from src.database import async_session_local


async def get_async_session():
    async with async_session_local() as session:
        yield session


AsyncSession = Annotated[AsyncLocalSession, Depends(get_async_session)]
