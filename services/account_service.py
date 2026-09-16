from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.db import get_session
from models.account import Account


def get_all_accounts() -> list[Account]:
    with get_session() as session:
        return list(
            session.scalars(select(Account).options(joinedload(Account.category)))
        )


def create_account(name: str, category_id: int, balance: float) -> None:
    with get_session() as session:
        account = Account(name=name, category_id=category_id, balance=balance)
        session.add(account)
        session.commit()
