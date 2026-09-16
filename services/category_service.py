from sqlalchemy import select

from database.db import get_session
from models.category import Category


def get_all_categories() -> list[Category]:
    with get_session() as session:
        return list(session.scalars(select(Category)))


def create_category(name: str) -> None:
    with get_session() as session:
        category = Category(name=name)
        session.add(category)
        session.commit()
