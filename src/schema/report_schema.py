from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    plant_condition: int = Field(ge=1, le=5)
    pest_condition: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=200)
