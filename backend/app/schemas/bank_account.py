from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BankAccountBase(BaseModel):
    villager_id: int
    account_holder: str
    bank_name: Optional[str] = None
    bank_branch: Optional[str] = None
    account_number_encrypted: Optional[str] = None
    account_type: Optional[str] = None
    is_active: Optional[int] = 1
    remark: Optional[str] = None

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountUpdate(BankAccountBase):
    pass

class BankAccountOut(BankAccountBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
