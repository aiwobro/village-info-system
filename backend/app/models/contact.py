from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Contact(Base):
    """联系方式"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    villager_id = Column(Integer, ForeignKey("villagers.id"), nullable=False, comment="关联村民")
    phone = Column(String(20), comment="手机号")
    backup_phone = Column(String(20), comment="备用电话")
    wechat = Column(String(100), comment="微信号")
    qq = Column(String(50), comment="QQ号")
    email = Column(String(100), comment="邮箱")
    emergency_contact = Column(String(100), comment="紧急联系人")
    emergency_phone = Column(String(20), comment="紧急联系人电话")
    remark = Column(Text, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
