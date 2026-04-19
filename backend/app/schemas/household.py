from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HouseholdBase(BaseModel):
    household_no: str
    natural_village_id: int
    head_id: Optional[int] = None
    address: Optional[str] = None


class HouseholdCreate(HouseholdBase):
    pass


class HouseholdUpdate(HouseholdBase):
    pass


class HouseholdOut(HouseholdBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    head_name: Optional[str] = None
    member_count: int = 0

    class Config:
        from_attributes = True
