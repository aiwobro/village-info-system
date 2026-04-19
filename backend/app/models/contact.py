from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Contact(Base):
    """联系方式"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    villager_id = Column(Integer, ForeignKey("villagers.id"), nullable=False, comment="关联村民")
    type = Column(String(20), nullable=False, comment="类型: phone/wechat/qq/email")
    value = Column(String(100), nullable=False, comment="联系方式值")
    is_primary = Column(Integer, default=0, comment="是否主要联系方式")
    remark = Column(String(200), comment="备注")

    # 关联
    villager = relationship("Villager", back_populates="contacts")
