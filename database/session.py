from typing import Generator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from config import DB_URL, DB_ECHO

engine = create_async_engine(DB_URL, future=True, echo=DB_ECHO)

async_session = async_sessionmaker(engine, expire_on_commit=False)


# async def get_async_session() -> AsyncSession:
#     """Dependency for getting async session"""
#     async with async_session() as session:
#         return session
