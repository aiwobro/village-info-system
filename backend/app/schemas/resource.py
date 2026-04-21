from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ResourceBase(BaseModel):
    name: str
    code: Optional[str] = None
    resource_type: Optional[str] = None
    location: Optional[str] = None
    area: Optional[float] = None
    reserves: Optional[str] = None
    status: Optional[str] = "可用"
    development: Optional[str] = None
    natural_village_id: Optional[int] = None
    description: Optional[str] = None
    remark: Optional[str] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(ResourceBase):
    pass

class ResourceOut(ResourceBase):
    id: int
    is_locked: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ResourceBatchCreate(BaseModel):
    items: List[ResourceCreate]
