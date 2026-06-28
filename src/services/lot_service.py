import json
import os

from sqlalchemy.orm import Session

from models.lot import Lot
from repositories import lot_repository, report_repository
from schema.lot_schema import LotCreate, LotUpdate


def get_all_lots(db: Session) -> list[Lot]:
    return lot_repository.get_all(db)


def get_lot_by_id(db: Session, lot_id: str) -> Lot | None:
    return lot_repository.get_by_id(db, lot_id)


def create_lot(db: Session, data: LotCreate) -> Lot:
    return lot_repository.create(db, data)


def update_lot(db: Session, lot_id: str, data: LotUpdate) -> Lot | None:
    return lot_repository.update(db, lot_id, data)


def delete_lot(db: Session, lot_id: str) -> bool:
    """ロット削除。紐づくレポートと写真ファイルも削除する"""
    reports = report_repository.get_by_lot(db, lot_id)
    for report in reports:
        if report.photo_paths:
            paths = json.loads(report.photo_paths)
            for path in paths:
                if os.path.exists(path):
                    os.remove(path)
    report_repository.delete_by_lot(db, lot_id)
    return lot_repository.delete(db, lot_id)
