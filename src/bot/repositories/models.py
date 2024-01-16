import os

from sqlalchemy import String, Boolean, select, BigInteger, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
)

engine = create_engine('sqlite:///db.db', echo=os.getenv('DB_ECHO', False))
# engine = create_engine('sqlite:///db.db', echo=True)
db_session = Session(engine)


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    title: Mapped[str] = mapped_column(String(64))
    content: Mapped[str]
    is_done: Mapped[bool] = mapped_column(Boolean)
    tg_user_id: Mapped[int] = mapped_column(BigInteger)

    @classmethod
    def get_by_id(cls, todo_id: int):
        return db_session.query(Todo).filter_by(id=todo_id).first()

    @classmethod
    def get_all_for_user(cls, user_id: int):
        return db_session.query(Todo).filter_by(tg_user_id=user_id).all()

    @classmethod
    def get_active_for_user(cls, user_id: int):
        return db_session.query(Todo).filter_by(tg_user_id=user_id, is_done=False).all()

    @classmethod
    def create_for_user(cls, user_id: int, title: str, content: str, is_done: bool = False):
        todo = cls(
            title=title,
            content=content,
            tg_user_id=user_id,
            is_done=is_done,
        )
        db_session.add(todo)
        db_session.commit()

    @classmethod
    def mark_todo_as_done(cls, todo_id: int):
        todo = cls.get_by_id(todo_id)
        todo.is_done = True
        db_session.commit()

    @classmethod
    def delete(cls, todo_id: int):
        db_session.query(Todo).filter_by(id=todo_id).delete()


Todo.metadata.create_all(engine, checkfirst=True)
