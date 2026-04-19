from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class VillagerBase(BaseModel):
    name: str
    id_card: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    ethnicity: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    relation_to_head: Optional[str] = None
    household_id: Optional[int] = None
    address: Optional[str] = None
    remark: Optional[str] = None


class VillagerCreate(VillagerBase):
    pass


class VillagerUpdate(VillagerBase):
    pass


class VillagerOut(VillagerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class VillagerBatchCreate(BaseModel):
    items: List[VillagerCreate]
