from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class AdminVillage(Base):
    """行政村"""
    __tablename__ = "admin_villages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="村名")
    code = Column(String(50), unique=True, comment="行政区划码")
    leader = Column(String(100), comment="村支书/村主任")
    phone = Column(String(20), comment="联系电话")
    address = Column(String(200), comment="地址")
    description = Column(Text, comment="描述")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
