from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class BankAccount(Base):
    """银行账号"""
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    villager_id = Column(Integer, ForeignKey("villagers.id"), nullable=False, comment="关联村民")
    bank_name = Column(String(100), nullable=False, comment="开户行")
    account_number_encrypted = Column(Text, comment="卡号(加密存储)")
    account_holder = Column(String(100), nullable=False, comment="开户名")
    account_type = Column(String(50), comment="账户类型: personal/corporate")
    is_active = Column(Integer, default=1, comment="是否有效 0否 1是")
    remark = Column(String(200), comment="备注")

    # 关联
    villager = relationship("Villager", back_populates="bank_accounts")
