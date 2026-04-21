from pydantic import BaseModel
from typing import List, Optional


class ContactBase(BaseModel):
    villager_id: int
    type: str
    value: str
    is_primary: Optional[int] = 0
    remark: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactOut(ContactBase):
    id: int
    is_locked: int = 0

    class Config:
        from_attributes = True

class ContactBatchCreate(BaseModel):
    items: List[ContactCreate]
