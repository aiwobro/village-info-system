from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VillagerBase(BaseModel):
    name: str
    id_card: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    age: Optional[int] = None
    ethnicity: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    household_relation: Optional[str] = None
    is_householder: Optional[int] = 0
    household_id: Optional[str] = None
    village_id: Optional[int] = None
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
