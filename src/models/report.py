from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, index=True)
    lot_id = Column(String, nullable=False)
    date = Column(String, nullable=False)
    plant_condition = Column(Integer, nullable=False)
    pest_condition = Column(Integer, nullable=False)
    # 写真パスのJSON配列（最大3枚）
    photo_paths = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
