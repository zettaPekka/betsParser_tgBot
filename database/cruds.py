from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm.attributes import flag_modified

from  database.models import User
from database.init_db import engine


session_factory = async_sessionmaker(engine)


async def create_user_if_not_exists(user_id: int):
    async with session_factory() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(user_id=user_id)
            session.add(user)
            await session.commit()

async def get_user_predict_filter(user_id: int):
    async with session_factory() as session:
        user = await session.get(User, user_id)
        return user.predict_filter

async def edit_user_predict_filter(user_id: int, filter_type: str, filter_type_data: str | list):
    async with session_factory() as session:
        user = await session.get(User, user_id)
        user.predict_filter[filter_type] = filter_type_data
        flag_modified(user, 'predict_filter')
        await session.commit()