from sqlalchemy import Column, Integer, String, Float, ForeignKey, Numeric, Text, Date, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Asset(Base):
    """村集体资产"""
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="资产名称")
    code = Column(String(100), comment="资产编码")
    asset_type = Column(String(50), comment="资产类型(土地/建筑/设备/设施)")
    description = Column(Text, comment="资产描述")
    location = Column(String(200), comment="位置")
    area = Column(Float, comment="面积(平方米)")
    quantity = Column(Float, default=1, comment="数量")
    unit = Column(String(20), comment="单位")
    purchase_date = Column(String(20), comment="购置日期")
    purchase_price = Column(Numeric(15, 2), comment="购置价格")
    current_value = Column(Numeric(15, 2), comment="当前估值")
    status = Column(String(50), default="正常使用", comment="状态(正常使用/报废/出租)")
    villager_id = Column(Integer, ForeignKey("villagers.id"), comment="负责人")
    remark = Column(Text, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
