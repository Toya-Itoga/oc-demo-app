from sqlalchemy.orm import Session

from models.lot import Lot
from schema.lot_schema import LotCreate, LotUpdate


def get_all(db: Session) -> list[Lot]:
    return db.query(Lot).all()


def get_by_id(db: Session, lot_id: str) -> Lot | None:
    return db.query(Lot).filter(Lot.id == lot_id).first()


def create(db: Session, data: LotCreate) -> Lot:
    lot = Lot(
        id=data.id,
        farm_name=data.farm_name,
        house_number=data.house_number,
        crop_type=data.crop_type,
        crop_variety=data.crop_variety,
        plant_count=data.plant_count,
    )
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return lot


def update(db: Session, lot_id: str, data: LotUpdate) -> Lot | None:
    lot = get_by_id(db, lot_id)
    if not lot:
        return None
    lot.farm_name = data.farm_name
    lot.house_number = data.house_number
    lot.crop_type = data.crop_type
    lot.crop_variety = data.crop_variety
    lot.plant_count = data.plant_count
    db.commit()
    db.refresh(lot)
    return lot


def delete(db: Session, lot_id: str) -> bool:
    lot = get_by_id(db, lot_id)
    if not lot:
        return False
    db.delete(lot)
    db.commit()
    return True
