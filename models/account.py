from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.category import Category


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default="")
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    balance: Mapped[float] = mapped_column(default=0)

    category: Mapped["Category"] = relationship()
