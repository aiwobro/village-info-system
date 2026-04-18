from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Villager(Base):
    """村民信息"""
    __tablename__ = "villagers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, comment="姓名")
    id_card = Column(String(18), unique=True, comment="身份证号")
    gender = Column(String(10), comment="性别")
    birth_date = Column(String(20), comment="出生日期")
    age = Column(Integer, comment="年龄")
    ethnicity = Column(String(50), comment="民族")
    education = Column(String(50), comment="文化程度")
    occupation = Column(String(100), comment="职业")
    household_relation = Column(String(50), comment="与户主关系")
    is_householder = Column(Integer, default=0, comment="是否户主 0否 1是")
    household_id = Column(String(50), index=True, comment="户号")
    village_id = Column(Integer, ForeignKey("villages.id"), comment="所属村庄")
    address = Column(String(200), comment="住址")
    remark = Column(Text, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
