from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class NaturalVillage(Base):
    """自然村"""
    __tablename__ = "natural_villages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="村名")
    admin_village_id = Column(Integer, ForeignKey("admin_villages.id"), nullable=False, comment="所属行政村")
    leader = Column(String(100), comment="组长")
    phone = Column(String(20), comment="联系电话")
    description = Column(Text, comment="描述")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联
    admin_village = relationship("AdminVillage", backref="natural_villages")
    households = relationship("Household", back_populates="natural_village")
    resources = relationship("Resource", back_populates="natural_village")
