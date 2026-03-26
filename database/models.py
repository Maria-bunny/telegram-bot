from sqlalchemy import String, Integer, Boolean, BigInteger, MetaData, Table, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession


engine = create_async_engine("sqlite+aiosqlite:///database/database.sql")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Texts(Base):
    __tablename__ = 'Texts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    thursday_text: Mapped[str] = mapped_column(String, default='---')
    sunday_text: Mapped[str] = mapped_column(String, default='---')
    every_day_text: Mapped[str] = mapped_column(String, default='---')
    thirst_day_text: Mapped[str] = mapped_column(String, default='---')


class Chats(Base):
    __tablename__ = 'Chats'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, default=0)
    chat_name: Mapped[str] = mapped_column(String, default='---')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)