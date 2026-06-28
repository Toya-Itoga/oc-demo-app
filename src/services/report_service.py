import json
import os

from sqlalchemy.orm import Session
from ulid import ULID

from models.report import Report
from repositories import report_repository
from utils.datetime_utils import get_now, get_today_str
from utils.demo_data import generate_ai_summary, generate_humidity, generate_temperature


def get_reports_by_lot(db: Session, lot_id: str) -> list[Report]:
    return report_repository.get_by_lot(db, lot_id)


def get_report_by_id(db: Session, report_id: str) -> Report | None:
    return report_repository.get_by_id(db, report_id)


def get_today_report(db: Session, lot_id: str) -> Report | None:
    return report_repository.get_by_lot_and_date(db, lot_id, get_today_str())


def create_or_update_report(
    db: Session,
    lot_id: str,
    crop_type: str,
    crop_variety: str | None,
    plant_condition: int,
    pest_condition: int,
    comment: str | None,
    photo_paths: list[str],
) -> Report:
    """当日レポートが既存なら更新、なければ新規作成する"""
    today = get_today_str()
    summary = generate_ai_summary(
        crop_type, crop_variety, plant_condition, pest_condition, comment
    )
    existing = report_repository.get_by_lot_and_date(db, lot_id, today)

    if existing:
        existing.plant_condition = plant_condition
        existing.pest_condition = pest_condition
        existing.comment = comment
        existing.ai_summary = summary
        existing.photo_paths = json.dumps(photo_paths) if photo_paths else None
        return report_repository.save(db, existing)

    report = Report(
        id=str(ULID()),
        lot_id=lot_id,
        date=today,
        plant_condition=plant_condition,
        pest_condition=pest_condition,
        comment=comment,
        ai_summary=summary,
        photo_paths=json.dumps(photo_paths) if photo_paths else None,
        temperature=generate_temperature(),
        humidity=generate_humidity(),
        created_at=get_now(),
    )
    return report_repository.create(db, report)


def remove_photo(db: Session, report_id: str, photo_index: int) -> Report | None:
    """レポートから指定インデックスの写真を削除する"""
    report = report_repository.get_by_id(db, report_id)
    if not report:
        return None
    paths: list[str] = json.loads(report.photo_paths) if report.photo_paths else []
    if 0 <= photo_index < len(paths):
        target = paths.pop(photo_index)
        if os.path.exists(target):
            os.remove(target)
    report.photo_paths = json.dumps(paths) if paths else None
    return report_repository.save(db, report)
