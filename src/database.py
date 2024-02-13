from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import SQLALCHEMY_DATABASE_URL as SECRET_DATABASE_URL


SQLALCHEMY_DATABASE_URL = SECRET_DATABASE_URL
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
async_session_local = async_sessionmaker(async_engine, expire_on_commit=False)
