from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class AssetBase(BaseModel):
    name: str
    code: Optional[str] = None
    asset_type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    area: Optional[float] = None
    quantity: Optional[float] = 1
    unit: Optional[str] = None
    purchase_date: Optional[str] = None
    purchase_price: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    status: Optional[str] = "正常使用"
    villager_id: Optional[int] = None
    remark: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(AssetBase):
    pass

class AssetOut(AssetBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
