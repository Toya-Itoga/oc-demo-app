from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import SessionLocal, engine
from models import lot, report  # noqa: F401 — テーブル定義をインポートして create_all で認識させる
from database import Base
from routers import lots, reports
from utils.demo_data import DEMO_LOTS
from models.lot import Lot


@asynccontextmanager
async def lifespan(app: FastAPI):
    # テーブル作成
    Base.metadata.create_all(bind=engine)
    # デモロットの初期データ投入
    db = SessionLocal()
    try:
        if db.query(Lot).count() == 0:
            for data in DEMO_LOTS:
                db.add(Lot(**data))
            db.commit()
    finally:
        db.close()
    yield


app = FastAPI(title="農業日報管理アプリ", lifespan=lifespan)

# 静的ファイルのマウント
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/imgs", StaticFiles(directory="imgs"), name="imgs")

# ルーターの登録
app.include_router(lots.router)
app.include_router(reports.router)
