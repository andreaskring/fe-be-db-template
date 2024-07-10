from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from backend.config import get_settings
from backend.db import get_async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.extra["engine"].dispose()
    # Reflect the DB


settings = get_settings()
engine = get_async_engine(settings)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def async_db_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
        await session.aclose()

app = FastAPI(engine=engine, lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/category/{cat_id}")
async def category(
    cat_id: int,
    db_session: AsyncSession = Depends(async_db_session)
) -> dict:
    print("Hurra")
    result = await db_session.execute(text("SELECT * FROM category"))
    print(result)
    for row in result:
        print(row)

    return {"foo": "barx"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
