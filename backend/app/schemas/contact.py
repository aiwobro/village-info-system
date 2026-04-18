from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ContactBase(BaseModel):
    villager_id: int
    phone: Optional[str] = None
    backup_phone: Optional[str] = None
    wechat: Optional[str] = None
    qq: Optional[str] = None
    email: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    remark: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactOut(ContactBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
