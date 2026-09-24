from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("postgresql+asyncpg://postgres.ijhohmazwiphfmxaqlly:3451551184polerpo@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres", connect_args={"statement_cache_size": 0})

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

sessionDeb = Annotated[
    AsyncSession,
    Depends(
        get_session
    )
]

class Base(DeclarativeBase):
    pass