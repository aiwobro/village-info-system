from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class BankAccount(Base):
    """银行账号"""
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    villager_id = Column(Integer, ForeignKey("villagers.id"), nullable=False, comment="关联村民")
    account_holder = Column(String(100), nullable=False, comment="开户名")
    bank_name = Column(String(100), comment="开户行")
    bank_branch = Column(String(200), comment="支行名称")
    account_number_encrypted = Column(Text, comment="卡号(加密存储)")
    account_type = Column(String(50), comment="账户类型(个人/对公)")
    is_active = Column(Integer, default=1, comment="是否有效 0否 1是")
    remark = Column(Text, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
