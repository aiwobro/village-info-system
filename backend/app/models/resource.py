from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Resource(Base):
    """村集体资源"""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="资源名称")
    code = Column(String(100), comment="资源编码")
    resource_type = Column(String(50), comment="资源类型(森林/水源/矿产/农田/草地/水面)")
    location = Column(String(200), comment="位置")
    area = Column(Float, comment="面积(亩)")
    reserves = Column(String(100), comment="储量/产量")
    status = Column(String(50), default="可用", comment="状态(可用/开发中/已开发/保护)")
    development = Column(String(200), comment="开发利用情况")
    description = Column(Text, comment="描述")
    remark = Column(Text, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
