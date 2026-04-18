from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VillageBase(BaseModel):
    name: str
    code: Optional[str] = None
    address: Optional[str] = None
    area: Optional[float] = None
    population: Optional[int] = 0
    established_date: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None

class VillageCreate(VillageBase):
    pass

class VillageUpdate(VillageBase):
    pass

class VillageOut(VillageBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
