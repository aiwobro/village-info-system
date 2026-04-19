from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Household(Base):
    """户"""
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    household_no = Column(String(50), unique=True, nullable=False, comment="户号")
    natural_village_id = Column(Integer, ForeignKey("natural_villages.id"), nullable=False, comment="所属自然村")
    head_id = Column(Integer, ForeignKey("villagers.id"), comment="户主ID")
    address = Column(String(200), comment="住址")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联 - 明确指定 foreign_keys
    natural_village = relationship("NaturalVillage", back_populates="households")
    head = relationship("Villager", foreign_keys=[head_id], backref="households_as_head")
    villagers = relationship("Villager", back_populates="household", foreign_keys="Villager.household_id")
