from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Villager(Base):
    """村民"""
    __tablename__ = "villagers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, comment="姓名")
    id_card = Column(String(18), unique=True, comment="身份证号")
    gender = Column(String(10), comment="性别")
    birth_date = Column(String(20), comment="出生日期")
    ethnicity = Column(String(50), comment="民族")
    education = Column(String(50), comment="文化程度")
    occupation = Column(String(100), comment="职业")
    relation_to_head = Column(String(50), comment="与户主关系")  # 本人/配偶/子女/父母等
    household_id = Column(Integer, ForeignKey("households.id"), comment="所属户")
    address = Column(String(200), comment="住址")
    remark = Column(Text, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联
    household = relationship("Household", back_populates="villagers", foreign_keys=[household_id])
    contacts = relationship("Contact", back_populates="villager")
    bank_accounts = relationship("BankAccount", back_populates="villager")
