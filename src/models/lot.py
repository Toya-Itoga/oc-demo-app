from sqlalchemy import Column, Integer, String

from database import Base


class Lot(Base):
    __tablename__ = "lots"

    id = Column(String, primary_key=True, index=True)
    farm_name = Column(String, nullable=False)
    house_number = Column(String, nullable=False)
    crop_type = Column(String, nullable=False)
    crop_variety = Column(String, nullable=True)
    plant_count = Column(Integer, nullable=True)
