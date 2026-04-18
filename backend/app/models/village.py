from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Village(Base):
    """村庄基础信息"""
    __tablename__ = "villages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="村名")
    code = Column(String(50), unique=True, comment="村庄代码")
    address = Column(String(200), comment="地址")
    area = Column(Float, comment="面积(平方公里)")
    population = Column(Integer, default=0, comment="人口总数")
    established_date = Column(String(50), comment="成立时间")
    latitude = Column(Float, comment="纬度")
    longitude = Column(Float, comment="经度")
    description = Column(Text, comment="描述")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
