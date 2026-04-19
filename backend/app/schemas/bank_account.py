from pydantic import BaseModel
from typing import List, Optional


class BankAccountBase(BaseModel):
    villager_id: int
    bank_name: str
    account_number_encrypted: Optional[str] = None
    account_holder: str
    account_type: Optional[str] = None
    is_active: Optional[int] = 1
    remark: Optional[str] = None


class BankAccountCreate(BankAccountBase):
    pass


class BankAccountUpdate(BankAccountBase):
    pass


class BankAccountOut(BankAccountBase):
    id: int

    class Config:
        from_attributes = True

class BankAccountBatchCreate(BaseModel):
    items: List[BankAccountCreate]
