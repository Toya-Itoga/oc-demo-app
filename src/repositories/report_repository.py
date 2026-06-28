from sqlalchemy.orm import Session

from models.report import Report


def get_by_lot(db: Session, lot_id: str) -> list[Report]:
    """ロットに紐づく全レポートを日付降順で返す"""
    return (
        db.query(Report)
        .filter(Report.lot_id == lot_id)
        .order_by(Report.date.desc())
        .all()
    )


def get_by_id(db: Session, report_id: str) -> Report | None:
    return db.query(Report).filter(Report.id == report_id).first()


def get_by_lot_and_date(db: Session, lot_id: str, date: str) -> Report | None:
    """1ロット1日1レポートの検索"""
    return (
        db.query(Report)
        .filter(Report.lot_id == lot_id, Report.date == date)
        .first()
    )


def create(db: Session, report: Report) -> Report:
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def save(db: Session, report: Report) -> Report:
    """既存レポートを保存する（更新用）"""
    db.commit()
    db.refresh(report)
    return report


def delete_by_lot(db: Session, lot_id: str) -> None:
    """ロットに紐づく全レポートを削除する"""
    db.query(Report).filter(Report.lot_id == lot_id).delete()
    db.commit()
