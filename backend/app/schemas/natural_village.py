from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class NaturalVillageBase(BaseModel):
    name: str
    admin_village_id: int
    leader: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None


class NaturalVillageCreate(NaturalVillageBase):
    pass


class NaturalVillageUpdate(NaturalVillageBase):
    pass


class NaturalVillageOut(NaturalVillageBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NaturalVillageBatchCreate(BaseModel):
    items: List[NaturalVillageCreate]
