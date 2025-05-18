from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, JSON
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    predict_filter: Mapped[dict] = mapped_column(JSON, default={'sport':'Не указано', 'k':'Не указано', 'date':'Не указано'})
