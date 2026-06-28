import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 環境ごとにDBを分ける
ENV = os.getenv("APP_ENV", "development")
DB_FILE = "test.db" if ENV == "test" else "app.db"
DATABASE_URL = f"sqlite:///./{DB_FILE}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
