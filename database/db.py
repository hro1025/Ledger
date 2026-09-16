from pathlib import Path

from PySide6.QtCore import QStandardPaths
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from models.base import Base
from models.category import Category


def get_db_path() -> Path:
    app_data_dir: str = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppDataLocation
    )
    app_folder: Path = Path(app_data_dir) / "ApexFinance"
    app_folder.mkdir(parents=True, exist_ok=True)
    return app_folder / "apex.db"


engine: Engine = create_engine(url=f"sqlite:///{get_db_path()}")
Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    return Session(bind=engine)


DEFAULT_CATEGORIES = ["Checking", "Savings", "Credit Card", "Investment", "Cash"]


def seed_default_categories() -> None:
    with get_session() as session:
        existing = session.query(Category).first()
        if existing is None:
            for name in DEFAULT_CATEGORIES:
                session.add(Category(name=name))
            session.commit()


seed_default_categories()
