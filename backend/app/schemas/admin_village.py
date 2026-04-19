from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class AdminVillageBase(BaseModel):
    name: str
    code: Optional[str] = None
    leader: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None


class AdminVillageCreate(AdminVillageBase):
    pass


class AdminVillageUpdate(AdminVillageBase):
    pass


class AdminVillageOut(AdminVillageBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AdminVillageBatchCreate(BaseModel):
    items: List[AdminVillageCreate]
