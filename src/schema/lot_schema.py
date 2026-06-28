from typing import Optional

from pydantic import BaseModel


class LotCreate(BaseModel):
    id: str
    farm_name: str
    house_number: str
    crop_type: str
    crop_variety: Optional[str] = None
    plant_count: Optional[int] = None


class LotUpdate(BaseModel):
    farm_name: str
    house_number: str
    crop_type: str
    crop_variety: Optional[str] = None
    plant_count: Optional[int] = None
