from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from src.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**data).returning(cls.model)
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e